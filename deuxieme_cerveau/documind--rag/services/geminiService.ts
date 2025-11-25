
import { GoogleGenAI, Content, Part } from "@google/genai";
import { 
  GEMINI_FLASH_MODEL,
  GEMINI_PRO_MODEL,
  SYSTEM_INSTRUCTION, 
  PROMPT_PHASE_1_DECOMPOSITION,
  PROMPT_PHASE_2_SCOUTING,
  PROMPT_PHASE_3_EXTRACTION,
  PROMPT_PHASE_4_SYNTHESIS,
  PROMPT_PHASE_5_VERIFICATION,
  PROMPT_PHASE_6_FINAL,
  PROMPT_STAGE_2_SMART,
  PROMPT_STAGE_3_INSANITY
} from "../constants";
import { UploadedFile, OrchestrationPhase, SessionArtifact, Message, MessageRole } from "../types";
import { v4 as uuidv4 } from 'uuid';

let client: GoogleGenAI | null = null;

const getClient = (): GoogleGenAI => {
  if (!client) {
    const apiKey = process.env.API_KEY;
    if (!apiKey) {
      console.error("API_KEY is missing from environment variables.");
      throw new Error("API Key not found");
    }
    client = new GoogleGenAI({ apiKey });
  }
  return client;
};

interface OrchestrationCallbacks {
  onPhaseChange: (phase: OrchestrationPhase) => void;
  onLog: (log: string) => void;
  onStream: (text: string) => void;
  onArtifact: (artifact: SessionArtifact) => void;
}

export class GeminiService {
  
  constructor() {
    // Client is lazy loaded
  }

  /**
   * Helper to delay execution
   */
  private async delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * TRI-LAYER SEGMENTATION STRATEGY
   */
  private segmentContent(text: string, fileName: string, chunkSize: number = 4000): string {
    const extension = fileName.split('.').pop()?.toLowerCase() || '';
    
    // Default separators
    let separators = ["\n\n", "\n", " ", ""]; 
    
    // Specialized separators based on file type
    if (['md', 'markdown'].includes(extension)) {
      separators = ["\n# ", "\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""];
    } else if (['py'].includes(extension)) {
      separators = ["\nclass ", "\ndef ", "\n\n", "\n", " "];
    } else if (['js', 'jsx', 'ts', 'tsx', 'java', 'c', 'cpp', 'cs', 'go', 'rs', 'swift', 'php'].includes(extension)) {
       separators = ["\nclass ", "\nfunction ", "\ninterface ", "\nconst ", "\nlet ", "\nvar ", "\n\n", "\n", " "];
    }

    const chunks = this.recursiveSplit(text, separators, chunkSize);
    
    // --- LAYER 1: METADATA & TOPOLOGY SCAN ---
    const datePattern = /\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}\/\d{1,2}\/\d{2,4}\b/g;
    const dateMatches = text.match(datePattern);
    const distinctDates = dateMatches ? new Set(dateMatches).size : 0;
    
    const totalTokensApprox = Math.ceil(text.length / 4);
    const layer1 = `DOCUMENT METADATA:
- Filename: ${fileName}
- Type: ${extension}
- Size: ${text.length} characters
- Approx Tokens: ${totalTokensApprox}
- Total Sections: ${chunks.length}
- Structure Hints: ${distinctDates > 1 ? `Detected ${distinctDates} potential date-based entries. This might be a DISCRETE collection.` : 'Appears monolithic.'}`;

    // --- LAYER 2: STRUCTURAL MAP ---
    const layer2 = chunks.map((chunk, i) => {
        const lines = chunk.split('\n').filter(l => l.trim().length > 0);
        const preview = lines.length > 0 
            ? lines[0].substring(0, 80).replace(/\s+/g, ' ') 
            : chunk.substring(0, 80).replace(/\s+/g, ' ');
        return `[Section ${i + 1}] Start: "${preview}..."`;
    }).join('\n');

    // --- LAYER 3: FULL CONTENT ---
    const layer3 = chunks.map((c, i) => `--- SECTION ${i + 1} ---\n${c}`).join('\n\n');
    
    return `*** LAYER 1: DOCUMENT METADATA ***\n${layer1}\n\n` + 
           `*** LAYER 2: STRUCTURAL CONTENT MAP ***\n(Use this map to locate relevant sections during the Scouting Phase)\n${layer2}\n\n` +
           `*** LAYER 3: FULL DOCUMENT CONTENT ***\n${layer3}\n\n` +
           `--- END OF DOCUMENT PROCESSING ---`;
  }

  private recursiveSplit(text: string, separators: string[], chunkSize: number): string[] {
    const finalChunks: string[] = [];
    let separator = separators[0];
    const nextSeparators = separators.length > 1 ? separators.slice(1) : [];
    
    if (separator === undefined) {
        for (let i = 0; i < text.length; i += chunkSize) {
            finalChunks.push(text.slice(i, i + chunkSize));
        }
        return finalChunks;
    }

    const parts = text.split(separator);
    let goodParts: string[] = [];

    for (const part of parts) {
        if (part.length > chunkSize) {
            if (nextSeparators.length > 0) {
              goodParts.push(...this.recursiveSplit(part, nextSeparators, chunkSize));
            } else {
              goodParts.push(...this.recursiveSplit(part, [], chunkSize)); 
            }
        } else {
            goodParts.push(part);
        }
    }

    let currentChunk = "";
    for (const part of goodParts) {
        let glue = "";
        if (separator.trim() === "") {
             glue = "";
        } else if (separator.includes("\n")) {
             glue = separator;
        } else {
             glue = "\n" + separator;
        }
        
        const potentialChunk = currentChunk ? (currentChunk + glue + part) : part;

        if (potentialChunk.length > chunkSize) {
            if (currentChunk) {
                finalChunks.push(currentChunk);
                currentChunk = part;
            } else {
                finalChunks.push(part);
                currentChunk = "";
            }
        } else {
            currentChunk = potentialChunk;
        }
    }
    
    if (currentChunk) {
        finalChunks.push(currentChunk);
    }

    return finalChunks;
  }

  /**
   * Helper to run a specific phase, stream result, and return the full text.
   */
  private async runPhase(
    client: GoogleGenAI,
    model: string,
    history: Content[],
    phase: OrchestrationPhase,
    prompt: string,
    callbacks: OrchestrationCallbacks,
    customTitle?: string
  ): Promise<string> {
    
    callbacks.onPhaseChange(phase);
    callbacks.onStream(""); // Clear buffer

    // Add the specific phase prompt to history for this call
    const currentInput: Content = {
        role: "user",
        parts: [{ text: prompt }]
    };

    const config = {
        systemInstruction: SYSTEM_INSTRUCTION
    };
    
    let fullText = "";

    try {
        // We use generateContentStream with the FULL history + new prompt
        const responseStream = await client.models.generateContentStream({
            model: model,
            contents: [...history, currentInput],
            config: config
        });

        for await (const chunk of responseStream) {
            const text = chunk.text;
            if (text) {
                fullText += text;
                callbacks.onStream(fullText);
            }
        }
    } catch (e) {
        console.error(`Error in ${phase}`, e);
        fullText = `[Error generating ${phase}: ${e}]`;
    }

    // Create Artifact
    const artifact: SessionArtifact = {
        id: uuidv4(),
        phase: phase,
        title: customTitle || phase, 
        content: fullText,
        timestamp: new Date(),
        model: model
    };
    callbacks.onArtifact(artifact);
    callbacks.onLog(`Completed ${phase} using ${model}`);

    return fullText;
  }

  /**
   * The core Orchestrator. 
   */
  public async orchestrateDeepAnalysis(
    message: string, 
    file: UploadedFile | null,
    previousMessages: Message[],
    callbacks: OrchestrationCallbacks
  ): Promise<string> {
    
    const client = getClient();
    
    // --- 0. CONTEXT PREPARATION ---
    const history: Content[] = [];

    // Inject File Context
    if (file) {
         const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
         
         if (isPdf) {
            history.push({
                role: "user",
                parts: [
                    { inlineData: { mimeType: "application/pdf", data: file.base64Data } },
                    { text: "SYSTEM INJECTION: PDF Document Loaded. Treat this as the absolute source of truth. Use Page Numbers for citations." }
                ]
            });
         } else {
            try {
              const binaryStr = atob(file.base64Data);
              const bytes = new Uint8Array(binaryStr.length);
              for (let i = 0; i < binaryStr.length; i++) {
                bytes[i] = binaryStr.charCodeAt(i);
              }
              const rawText = new TextDecoder().decode(bytes);
              const segmentedContext = this.segmentContent(rawText, file.name);
              
              history.push({
                role: "user",
                parts: [{ text: `SYSTEM INJECTION: Document Loaded.\n\n${segmentedContext}` }]
              });
            } catch (e) {
                // Fallback
                history.push({
                    role: "user",
                    parts: [
                        { inlineData: { mimeType: file.type || "text/plain", data: file.base64Data } },
                        { text: "Analyze this document." }
                    ]
                });
            }
         }
         history.push({ role: "model", parts: [{ text: "Acknowledged. I have read the document and am ready for deep analysis." }] });
    }

    // --- REBUILD HISTORY ---
    for (const msg of previousMessages) {
        history.push({
            role: msg.role === MessageRole.USER ? 'user' : 'model',
            parts: [{ text: msg.content }]
        });
    }

    // --- BRANCHING LOGIC FOR STAGES ---
    
    // STAGE 2: SMART ENRICHMENT
    if (message === PROMPT_STAGE_2_SMART) {
        callbacks.onLog("Initializing Stage 2: Smart Strategy (Gemini 3 Pro)...");
        const smartOutput = await this.runPhase(
            client, GEMINI_PRO_MODEL, history,
            OrchestrationPhase.SMART_ENRICHMENT,
            PROMPT_STAGE_2_SMART,
            callbacks,
            "STAGE_2_Smart_Strategy"
        );
        callbacks.onPhaseChange(OrchestrationPhase.COMPLETE);
        return smartOutput;
    }

    // STAGE 3: INSANITY MODE
    if (message === PROMPT_STAGE_3_INSANITY) {
        callbacks.onLog("Initializing Stage 3: Insanity Mode (Gemini 3 Pro)...");
        const insanityOutput = await this.runPhase(
            client, GEMINI_PRO_MODEL, history,
            OrchestrationPhase.INSANITY_MODE,
            PROMPT_STAGE_3_INSANITY,
            callbacks,
            "STAGE_3_Insanity_Plan"
        );
        callbacks.onPhaseChange(OrchestrationPhase.COMPLETE);
        return insanityOutput;
    }

    // DEFAULT: STAGE 1 (FULL 6-PHASE ANALYSIS)
    // Add Initial User Query
    history.push({ role: "user", parts: [{ text: message }] });

    // --- PHASE 1: DECOMPOSITION (Flash) ---
    callbacks.onLog("Initializing Phase 1: Decomposition...");
    const p1Output = await this.runPhase(
        client, GEMINI_FLASH_MODEL, history, 
        OrchestrationPhase.PHASE_1_DECOMPOSITION, 
        PROMPT_PHASE_1_DECOMPOSITION, callbacks
    );
    history.push({ role: "model", parts: [{ text: p1Output }] });
    await this.delay(500);

    // --- PHASE 2: SCOUTING (Flash) ---
    callbacks.onLog("Initializing Phase 2: Scouting...");
    const p2Output = await this.runPhase(
        client, GEMINI_FLASH_MODEL, history, 
        OrchestrationPhase.PHASE_2_SCOUTING, 
        PROMPT_PHASE_2_SCOUTING, callbacks
    );
    history.push({ role: "model", parts: [{ text: p2Output }] });
    await this.delay(500);

    // --- PHASE 3: EXTRACTION (Flash) ---
    callbacks.onLog("Initializing Phase 3: Extraction...");
    const p3Output = await this.runPhase(
        client, GEMINI_FLASH_MODEL, history, 
        OrchestrationPhase.PHASE_3_EXTRACTION, 
        PROMPT_PHASE_3_EXTRACTION, callbacks
    );
    history.push({ role: "model", parts: [{ text: p3Output }] });
    await this.delay(500);

    // --- PHASE 4: SYNTHESIS (Flash) ---
    callbacks.onLog("Initializing Phase 4: Synthesis...");
    const p4Output = await this.runPhase(
        client, GEMINI_FLASH_MODEL, history, 
        OrchestrationPhase.PHASE_4_SYNTHESIS, 
        PROMPT_PHASE_4_SYNTHESIS, callbacks
    );
    history.push({ role: "model", parts: [{ text: p4Output }] });
    await this.delay(500);

    // --- PHASE 5: VERIFICATION (Pro) ---
    callbacks.onLog("Initializing Phase 5: Verification (Gemini 3 Pro)...");
    const p5Output = await this.runPhase(
        client, GEMINI_PRO_MODEL, history, 
        OrchestrationPhase.PHASE_5_VERIFICATION, 
        PROMPT_PHASE_5_VERIFICATION, callbacks
    );
    history.push({ role: "model", parts: [{ text: p5Output }] });
    await this.delay(500);

    // --- PHASE 6: FINAL POLISH (Pro) ---
    callbacks.onLog("Initializing Phase 6: Final Polish (Gemini 3 Pro)...");
    const finalOutput = await this.runPhase(
        client, GEMINI_PRO_MODEL, history, 
        OrchestrationPhase.PHASE_6_FINAL_POLISH, 
        PROMPT_PHASE_6_FINAL, callbacks
    );
    
    callbacks.onPhaseChange(OrchestrationPhase.COMPLETE);
    callbacks.onLog("Deep Analysis Complete.");

    return finalOutput;
  }
}
