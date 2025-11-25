
import React, { useState, useRef, useEffect } from 'react';
import { Header } from './components/Header';
import { FileUpload } from './components/FileUpload';
import { ChatInterface } from './components/ChatInterface';
import { HistoryDrawer } from './components/HistoryDrawer';
import { GeminiService } from './services/geminiService';
import { UploadedFile, Message, MessageRole, ThinkingState, OrchestrationPhase, SessionArtifact, WorkflowStage, SavedSession } from './types';
import { PROMPT_STAGE_1_ANALYSE, PROMPT_STAGE_2_SMART, PROMPT_STAGE_3_INSANITY } from './constants';
import { v4 as uuidv4 } from 'uuid';
import { Clock, ArrowRight, FileText } from 'lucide-react';

const STORAGE_KEY_MESSAGES = 'documind_messages';
const STORAGE_KEY_ARTIFACTS = 'documind_artifacts';
const STORAGE_KEY_STAGE = 'documind_stage';
const STORAGE_KEY_HISTORY = 'documind_history';

const App: React.FC = () => {
  const [file, setFile] = useState<UploadedFile | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [thinkingState, setThinkingState] = useState<ThinkingState | null>(null);
  const [workflowStage, setWorkflowStage] = useState<WorkflowStage>(WorkflowStage.IDLE);
  const [history, setHistory] = useState<SavedSession[]>([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  
  // Refs for async state updates
  const currentLogsRef = useRef<string[]>([]);
  const currentArtifactsRef = useRef<SessionArtifact[]>([]);
  const geminiServiceRef = useRef<GeminiService | null>(null);

  // --- PERSISTENCE: LOAD ON MOUNT ---
  useEffect(() => {
    try {
      const savedMessages = localStorage.getItem(STORAGE_KEY_MESSAGES);
      const savedArtifacts = localStorage.getItem(STORAGE_KEY_ARTIFACTS);
      const savedStage = localStorage.getItem(STORAGE_KEY_STAGE);
      const savedHistory = localStorage.getItem(STORAGE_KEY_HISTORY);

      if (savedMessages) {
        // Need to revive dates
        const parsedMessages = JSON.parse(savedMessages).map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp)
        }));
        setMessages(parsedMessages);
      }

      if (savedArtifacts) {
        const parsedArtifacts = JSON.parse(savedArtifacts).map((a: any) => ({
          ...a,
          timestamp: new Date(a.timestamp)
        }));
        currentArtifactsRef.current = parsedArtifacts;
        // Restore thinking state to show artifacts if we have any
        if (parsedArtifacts.length > 0) {
            setThinkingState({
                phase: OrchestrationPhase.COMPLETE,
                logs: ["Session restored from local storage."],
                progress: 100,
                currentStreamText: "Session restored.",
                artifacts: parsedArtifacts
            });
        }
      }

      if (savedStage) {
        setWorkflowStage(parseInt(savedStage));
      }

      if (savedHistory) {
         setHistory(JSON.parse(savedHistory));
      }

    } catch (e) {
      console.error("Failed to restore session", e);
    }
  }, []);

  // --- PERSISTENCE: SAVE ON CHANGE ---
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY_MESSAGES, JSON.stringify(messages));
    localStorage.setItem(STORAGE_KEY_STAGE, workflowStage.toString());
  }, [messages, workflowStage]);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY_HISTORY, JSON.stringify(history));
  }, [history]);

  const saveArtifacts = (artifacts: SessionArtifact[]) => {
      localStorage.setItem(STORAGE_KEY_ARTIFACTS, JSON.stringify(artifacts));
  }

  // Helper to Archive Current Session
  const saveCurrentSessionToHistory = () => {
     if (messages.length === 0) return;

     const title = messages.find(m => m.role === MessageRole.USER)?.content.substring(0, 30) + "..." || "Untitled Session";
     const newSession: SavedSession = {
         id: uuidv4(),
         title: title,
         date: new Date().toISOString(),
         fileName: file?.name || "Unknown File",
         messages: messages,
         artifacts: currentArtifactsRef.current,
         workflowStage: workflowStage
     };

     setHistory(prev => [newSession, ...prev]);
  };

  const handleFileUpload = (uploadedFile: UploadedFile) => {
    // If there is an existing session, archive it before starting new
    if (messages.length > 0) {
        saveCurrentSessionToHistory();
        handleClearChat(false); // Clear but don't delete history
    }
    
    setFile(uploadedFile);
    geminiServiceRef.current = new GeminiService();
  };

  const handleClearChat = (archive = true) => {
    if (archive && messages.length > 0) {
        saveCurrentSessionToHistory();
    }

    setFile(null);
    setMessages([]);
    setThinkingState(null);
    setWorkflowStage(WorkflowStage.IDLE);
    currentLogsRef.current = [];
    currentArtifactsRef.current = [];
    geminiServiceRef.current = null;
    
    // Clear current session storage
    localStorage.removeItem(STORAGE_KEY_MESSAGES);
    localStorage.removeItem(STORAGE_KEY_ARTIFACTS);
    localStorage.removeItem(STORAGE_KEY_STAGE);
  };

  const handleRestoreSession = (session: SavedSession) => {
      // Archive current if active
      if (messages.length > 0) {
          saveCurrentSessionToHistory();
      }

      // Restore
      // Revive dates for messages
      const revivedMessages = session.messages.map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp)
      }));
      setMessages(revivedMessages);

      // Revive dates for artifacts
      const revivedArtifacts = session.artifacts.map((a: any) => ({
          ...a,
          timestamp: new Date(a.timestamp)
      }));
      currentArtifactsRef.current = revivedArtifacts;
      saveArtifacts(revivedArtifacts);

      setWorkflowStage(session.workflowStage);
      
      // Set thinking state to show artifacts
      if (revivedArtifacts.length > 0) {
        setThinkingState({
            phase: OrchestrationPhase.COMPLETE,
            logs: ["Session restored from history."],
            progress: 100,
            currentStreamText: "Session restored from archive.",
            artifacts: revivedArtifacts
        });
      } else {
        setThinkingState(null);
      }
      
      // Fake file object for display (we don't store base64 in history to save space)
      setFile({
          name: session.fileName,
          type: "application/pdf", // Assume PDF or generic
          size: 0,
          base64Data: "" // Empty, so re-analysis might fail without re-upload, but viewing is fine
      });

      // We need a service instance even if file is empty
      geminiServiceRef.current = new GeminiService();
  };

  const handleDeleteSession = (id: string) => {
      setHistory(prev => prev.filter(s => s.id !== id));
  };

  const handleSendMessage = async (triggerCode: string) => {
    if (!geminiServiceRef.current) {
        geminiServiceRef.current = new GeminiService();
    }
    
    if (!file && messages.length === 0) return;

    let actualPrompt = "";
    let nextStage = workflowStage;

    if (triggerCode === "STAGE_1") {
        actualPrompt = PROMPT_STAGE_1_ANALYSE;
        setWorkflowStage(WorkflowStage.ANALYZING);
        nextStage = WorkflowStage.ANALYSIS_COMPLETE;
    } else if (triggerCode === "STAGE_2") {
        actualPrompt = PROMPT_STAGE_2_SMART;
        setWorkflowStage(WorkflowStage.SMART_ENRICHING);
        nextStage = WorkflowStage.SMART_COMPLETE;
    } else if (triggerCode === "STAGE_3") {
        actualPrompt = PROMPT_STAGE_3_INSANITY;
        setWorkflowStage(WorkflowStage.INSANITY_RUNNING);
        nextStage = WorkflowStage.INSANITY_COMPLETE;
    } else {
        actualPrompt = triggerCode;
    }

    let displayContent = "";
    if (triggerCode === "STAGE_1") displayContent = "▶️ Running Stage 1: Structural Analysis...";
    else if (triggerCode === "STAGE_2") displayContent = "▶️ Running Stage 2: Strategic Enrichment (5-Level Reasoning)...";
    else if (triggerCode === "STAGE_3") displayContent = "▶️ Running Stage 3: Financial Impact & Insanity Mode...";
    else displayContent = actualPrompt;

    const userMsg: Message = {
      id: uuidv4(),
      role: MessageRole.USER,
      content: displayContent,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    currentLogsRef.current = [];
    setThinkingState({
      phase: OrchestrationPhase.IDLE,
      logs: [],
      progress: 0,
      currentStreamText: "",
      artifacts: currentArtifactsRef.current
    });

    try {
      const responseText = await geminiServiceRef.current.orchestrateDeepAnalysis(
        actualPrompt, 
        file, 
        messages, 
        {
           onPhaseChange: (phase) => {
               // Only update progress for full runs, stage 2/3 jumps to end
               const phases = Object.values(OrchestrationPhase);
               const phaseIndex = phases.indexOf(phase);
               const progress = Math.min(100, Math.max(5, (phaseIndex / 6) * 100));
               
               setThinkingState(prev => prev ? { ...prev, phase, progress } : null);
           },
           onLog: (log) => {
               currentLogsRef.current = [...currentLogsRef.current, log];
               setThinkingState(prev => prev ? { ...prev, logs: currentLogsRef.current } : null);
           },
           onStream: (text) => {
               setThinkingState(prev => prev ? { ...prev, currentStreamText: text } : null);
           },
           onArtifact: (artifact) => {
               currentArtifactsRef.current = [...currentArtifactsRef.current, artifact];
               saveArtifacts(currentArtifactsRef.current);
               setThinkingState(prev => prev ? { ...prev, artifacts: currentArtifactsRef.current } : null);
           }
        }
      );

      const botMsg: Message = {
        id: uuidv4(),
        role: MessageRole.MODEL,
        content: responseText,
        timestamp: new Date(),
        thinkingLogs: currentLogsRef.current
      };
      setMessages(prev => [...prev, botMsg]);
      setWorkflowStage(nextStage);

    } catch (error) {
      console.error(error);
      const errorMsg: Message = {
        id: uuidv4(),
        role: MessageRole.MODEL,
        content: "I encountered an error during the deep analysis process.",
        timestamp: new Date(),
        isError: true,
        thinkingLogs: currentLogsRef.current
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
      setThinkingState(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col font-sans text-slate-200 selection:bg-indigo-500/30">
      <Header onToggleHistory={() => setIsHistoryOpen(true)} />
      
      <HistoryDrawer 
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        sessions={history}
        onRestore={handleRestoreSession}
        onDelete={handleDeleteSession}
      />

      <main className="flex-1 flex flex-col max-w-6xl mx-auto w-full">
        {!file && messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-4 animate-in fade-in duration-500">
            <div className="text-center space-y-6 mb-12">
              <h1 className="text-5xl sm:text-6xl font-bold tracking-tight text-white drop-shadow-lg">
                Docu<span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Mind</span>
              </h1>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
                Advanced Reasoning Engine for your Documents.
                <br/>
                <span className="text-sm text-slate-500">Upload PDF, Code, or Text to begin the 3-Stage Expert Workflow.</span>
              </p>
            </div>
            
            <FileUpload onFileUpload={handleFileUpload} />
            
            {/* RECENT SESSIONS GRID - NEW ADDITION */}
            {history.length > 0 && (
                <div className="mt-16 w-full max-w-4xl px-4 animate-in slide-in-from-bottom-6 duration-700">
                    <div className="flex items-center gap-3 mb-6">
                        <Clock className="w-5 h-5 text-indigo-400" />
                        <h2 className="text-lg font-semibold text-slate-300">Recent Projects</h2>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {history.slice(0, 3).map((session) => (
                            <div 
                                key={session.id}
                                onClick={() => handleRestoreSession(session)}
                                className="bg-slate-900/40 border border-slate-800 p-5 rounded-xl hover:border-indigo-500/40 hover:bg-slate-900/80 cursor-pointer transition-all group shadow-lg"
                            >
                                <div className="flex justify-between items-start mb-3">
                                    <div className="p-2 bg-slate-800 rounded-lg group-hover:bg-indigo-500/20 group-hover:text-indigo-400 transition-colors text-slate-500">
                                        <FileText className="w-4 h-4" />
                                    </div>
                                    <span className="text-[10px] text-slate-500 font-mono bg-slate-950 px-2 py-1 rounded">
                                        {new Date(session.date).toLocaleDateString()}
                                    </span>
                                </div>
                                <h3 className="text-sm font-medium text-slate-200 mb-1 truncate">{session.title}</h3>
                                <p className="text-xs text-slate-500 truncate mb-4">{session.fileName}</p>
                                <div className="flex items-center text-xs text-indigo-400 font-medium opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0 duration-300">
                                    Resume Workspace <ArrowRight className="w-3 h-3 ml-1" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-16 max-w-5xl w-full px-4 border-t border-slate-800/50 pt-16">
               {[
                 { title: "Stage 1: Analyse", desc: "Structural Decomposition & Discrete Project Separation." },
                 { title: "Stage 2: Smart Enrich", desc: "5-Level Action-Reaction Strategic Reasoning." },
                 { title: "Stage 3: Insanity", desc: "Maximum Value Extraction & Financial Impact Analysis." }
               ].map((item, i) => (
                 <div key={i} className="bg-slate-900/30 p-4 rounded-xl border border-slate-800/50 hover:border-slate-700 transition-colors">
                   <h3 className="font-semibold text-slate-400 text-sm mb-1">{item.title}</h3>
                   <p className="text-xs text-slate-500">{item.desc}</p>
                 </div>
               ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 bg-slate-900 shadow-2xl shadow-black border border-slate-800 sm:rounded-2xl sm:my-6 sm:overflow-hidden animate-in slide-in-from-bottom-4 duration-500 flex flex-col">
            <ChatInterface 
              messages={messages}
              file={file || { name: "Session Restored", type: "unknown", size: 0, base64Data: "" }}
              isLoading={isLoading}
              thinkingState={thinkingState}
              workflowStage={workflowStage}
              onSendMessage={handleSendMessage}
              onClearChat={() => handleClearChat(true)}
            />
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
