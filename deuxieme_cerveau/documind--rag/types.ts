
export enum MessageRole {
  USER = 'user',
  MODEL = 'model',
  SYSTEM = 'system'
}

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  isError?: boolean;
  thinkingLogs?: string[]; // Log of the internal thought process
}

export interface UploadedFile {
  name: string;
  type: string;
  size: number;
  base64Data: string;
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  file: UploadedFile | null;
}

export enum OrchestrationPhase {
  IDLE = 'idle',
  PHASE_1_DECOMPOSITION = 'Decomposing & Planning',
  PHASE_2_SCOUTING = 'Scouting Document Sections',
  PHASE_3_EXTRACTION = 'Extracting Raw Evidence',
  PHASE_4_SYNTHESIS = 'Drafting Synthesis',
  PHASE_5_VERIFICATION = 'Verifying & Critiquing',
  PHASE_6_FINAL_POLISH = 'Finalizing Response',
  SMART_ENRICHMENT = 'Smart Strategy (Level 5)',
  INSANITY_MODE = 'Insanity Financial Plan',
  COMPLETE = 'Complete'
}

export interface SessionArtifact {
  id: string;
  phase: OrchestrationPhase;
  title: string;
  content: string; // The full text content of this artifact
  timestamp: Date;
  model: string;
}

export interface ThinkingState {
  phase: OrchestrationPhase;
  logs: string[];
  progress: number; // 0 to 100
  currentStreamText: string; // Real-time token stream
  artifacts: SessionArtifact[]; // Generated files
}

export enum WorkflowStage {
  IDLE = 0,
  ANALYZING = 1,
  ANALYSIS_COMPLETE = 2,
  SMART_ENRICHING = 3,
  SMART_COMPLETE = 4,
  INSANITY_RUNNING = 5,
  INSANITY_COMPLETE = 6
}

export interface SavedSession {
  id: string;
  title: string;
  date: string; // ISO string
  fileName: string;
  messages: Message[];
  artifacts: SessionArtifact[];
  workflowStage: WorkflowStage;
}
