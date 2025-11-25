
import React, { useRef, useEffect, useState } from 'react';
import { BrainCircuit, CheckCircle2, Search, FileSearch, PenTool, Gavel, Sparkles, Cpu, Terminal, FileText, Download, Archive, Loader2 } from 'lucide-react';
import { OrchestrationPhase, ThinkingState, SessionArtifact } from '../types';
import { GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL } from '../constants';
import JSZip from 'jszip';

interface ThinkingProcessProps {
  state: ThinkingState;
}

export const ThinkingProcess: React.FC<ThinkingProcessProps> = ({ state }) => {
  const { phase, logs, progress, currentStreamText, artifacts } = state;
  const terminalRef = useRef<HTMLDivElement>(null);
  const [isZipping, setIsZipping] = useState(false);

  // Auto-scroll terminal
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [currentStreamText, logs]);

  const getPhaseIcon = (p: OrchestrationPhase) => {
    switch (p) {
      case OrchestrationPhase.PHASE_1_DECOMPOSITION: return <BrainCircuit className="w-4 h-4 text-indigo-400" />;
      case OrchestrationPhase.PHASE_2_SCOUTING: return <Search className="w-4 h-4 text-cyan-400" />;
      case OrchestrationPhase.PHASE_3_EXTRACTION: return <FileSearch className="w-4 h-4 text-amber-400" />;
      case OrchestrationPhase.PHASE_4_SYNTHESIS: return <PenTool className="w-4 h-4 text-purple-400" />;
      case OrchestrationPhase.PHASE_5_VERIFICATION: return <Gavel className="w-4 h-4 text-rose-400" />;
      case OrchestrationPhase.PHASE_6_FINAL_POLISH: return <Sparkles className="w-4 h-4 text-emerald-400" />;
      default: return <Cpu className="w-4 h-4 text-slate-500" />;
    }
  };

  const getModelName = () => {
    if ([OrchestrationPhase.PHASE_5_VERIFICATION, OrchestrationPhase.PHASE_6_FINAL_POLISH].includes(phase)) {
        return "Gemini 3 Pro";
    }
    return "Gemini 2.5 Flash";
  };

  const handleDownloadArtifact = (artifact: SessionArtifact) => {
    // Changed to text/plain and .txt extension
    const blob = new Blob([artifact.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    // Sanitize title for filename
    const safeTitle = artifact.title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    a.download = `${safeTitle}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadArchive = async () => {
    if (artifacts.length === 0) return;
    setIsZipping(true);
    try {
      const zip = new JSZip();
      
      // Add artifacts as .txt
      const artifactsFolder = zip.folder("analysis_phases");
      if (artifactsFolder) {
        artifacts.forEach(artifact => {
           const safeTitle = artifact.title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
           artifactsFolder.file(`${safeTitle}.txt`, artifact.content);
        });
      }

      // Add simple log summary
      const logContent = logs.join('\n');
      zip.file("process_logs.txt", logContent);

      const blob = await zip.generateAsync({type:"blob"});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      a.download = `DocuMind_Session_${timestamp}.zip`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

    } catch (e) {
      console.error("Failed to zip", e);
    } finally {
      setIsZipping(false);
    }
  };

  const isComplete = phase === OrchestrationPhase.COMPLETE;

  if (isComplete && logs.length === 0) return null;

  return (
    <div className="w-full max-w-4xl mx-auto my-6 gap-6 grid grid-cols-1 md:grid-cols-3 animate-in fade-in slide-in-from-top-2">
      
      {/* LEFT COL: Live Terminal & Logs */}
      <div className="md:col-span-2 flex flex-col gap-4">
        
        {/* Main Status Card */}
        <div className="bg-slate-950 rounded-xl border border-slate-800 shadow-2xl overflow-hidden ring-1 ring-slate-800/50">
          <div className="bg-slate-900/50 px-4 py-3 border-b border-slate-800 flex items-center justify-between backdrop-blur-sm">
            <div className="flex items-center space-x-3">
              <div className={`p-1.5 rounded-lg border border-slate-700 ${isComplete ? 'bg-emerald-900/20 border-emerald-500/30' : 'bg-slate-800'}`}>
                {isComplete ? <CheckCircle2 className="w-4 h-4 text-emerald-500" /> : <Terminal className="w-4 h-4 text-indigo-400 animate-pulse" />}
              </div>
              <div className="flex flex-col">
                <span className="font-semibold text-xs text-slate-200 uppercase tracking-wide flex items-center gap-2">
                    {isComplete ? "Execution Complete" : "Live Reasoning Engine"}
                    {!isComplete && <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping"></span>}
                </span>
                <span className="text-[10px] text-slate-500 font-mono flex items-center gap-1">
                     Running on <span className="text-indigo-400">{getModelName()}</span>
                </span>
              </div>
            </div>
            {!isComplete && (
              <span className="text-xs font-mono text-indigo-400 bg-indigo-500/10 px-2 py-1 rounded border border-indigo-500/20">{Math.round(progress)}%</span>
            )}
          </div>

          {/* Progress Bar */}
          {!isComplete && (
            <div className="w-full bg-slate-900 h-0.5 overflow-hidden relative">
              <div 
                className="absolute top-0 left-0 h-full bg-gradient-to-r from-indigo-500 to-cyan-400 transition-all duration-500 ease-out shadow-[0_0_10px_rgba(99,102,241,0.5)]"
                style={{ width: `${progress}%` }}
              />
            </div>
          )}

          {/* LIVE TERMINAL */}
          <div 
            ref={terminalRef}
            className="p-4 bg-black font-mono text-xs h-64 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-800 scrollbar-track-transparent border-b border-slate-800"
          >
             <div className="text-emerald-500/50 mb-2 select-none">
                // System Output Stream...
             </div>
             {currentStreamText ? (
                <div className="whitespace-pre-wrap text-emerald-400 leading-relaxed">
                   {currentStreamText}
                   <span className="inline-block w-2 h-4 bg-emerald-500 ml-1 animate-pulse align-middle"></span>
                </div>
             ) : (
                <div className="text-slate-600 italic">
                   {isComplete ? "Session closed." : "Awaiting model token stream..."}
                </div>
             )}
          </div>

          {/* Logs Footer */}
          <div className="bg-slate-900 p-2 text-[10px] font-mono text-slate-500 flex items-center justify-between border-t border-slate-800">
             <span>Phase: {phase}</span>
             <span>Ops: {logs.length}</span>
          </div>
        </div>
      </div>

      {/* RIGHT COL: Artifacts / Data Folder */}
      <div className="md:col-span-1">
        <div className="bg-slate-950 rounded-xl border border-slate-800 shadow-xl overflow-hidden h-full flex flex-col">
            <div className="bg-slate-900/50 px-4 py-3 border-b border-slate-800 flex items-center gap-2 justify-between">
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4 text-slate-400" />
                  <span className="font-semibold text-xs text-slate-200 uppercase tracking-wide">Session Data</span>
                </div>
            </div>
            
            <div className="flex-1 p-3 space-y-2 overflow-y-auto max-h-[300px] scrollbar-thin">
                {artifacts.length === 0 ? (
                    <div className="text-center py-8 text-slate-600 text-xs">
                        No artifacts generated yet.
                    </div>
                ) : (
                    artifacts.map((artifact) => (
                        <div 
                          key={artifact.id} 
                          onClick={() => handleDownloadArtifact(artifact)}
                          className="group flex items-start gap-3 p-3 rounded-lg bg-slate-900/40 border border-slate-800 hover:border-indigo-500/30 hover:bg-slate-800/50 transition-all cursor-pointer"
                        >
                            <div className="mt-0.5">
                                {getPhaseIcon(artifact.phase)}
                            </div>
                            <div className="flex-1 min-w-0">
                                <h4 className="text-xs font-medium text-slate-300 truncate group-hover:text-indigo-300 transition-colors">
                                    {artifact.title}
                                </h4>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="text-[10px] text-slate-500 font-mono">
                                        {artifact.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                    <span className="text-[10px] px-1.5 rounded-full bg-slate-800 text-slate-500 border border-slate-700">
                                        {artifact.model.includes('flash') ? 'Flash' : 'Pro'}
                                    </span>
                                </div>
                            </div>
                            <Download className="w-3 h-3 text-slate-500 group-hover:text-indigo-400 transition-colors" />
                        </div>
                    ))
                )}
            </div>

            {/* DOWNLOAD ALL FOOTER */}
            <div className="p-3 border-t border-slate-800 bg-slate-900/30">
               <button
                 onClick={handleDownloadArchive}
                 disabled={artifacts.length === 0 || isZipping}
                 className={`w-full flex items-center justify-center gap-2 py-2 rounded-lg text-xs font-medium border transition-all
                   ${artifacts.length === 0 
                     ? 'bg-slate-900 text-slate-600 border-slate-800 cursor-not-allowed' 
                     : 'bg-indigo-600/10 text-indigo-300 border-indigo-500/30 hover:bg-indigo-600/20 hover:border-indigo-500/50 active:scale-95'
                   }`}
               >
                 {isZipping ? (
                   <>
                     <Loader2 className="w-3.5 h-3.5 animate-spin" />
                     <span>Compressing...</span>
                   </>
                 ) : (
                   <>
                     <Archive className="w-3.5 h-3.5" />
                     <span>Download Package (.zip)</span>
                   </>
                 )}
               </button>
            </div>
        </div>
      </div>

    </div>
  );
};
