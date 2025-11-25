
import React from 'react';
import { X, Clock, FileText, Trash2, ArrowRightCircle } from 'lucide-react';
import { SavedSession } from '../types';

interface HistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  sessions: SavedSession[];
  onRestore: (session: SavedSession) => void;
  onDelete: (sessionId: string) => void;
}

export const HistoryDrawer: React.FC<HistoryDrawerProps> = ({ 
  isOpen, 
  onClose, 
  sessions, 
  onRestore, 
  onDelete 
}) => {
  return (
    <>
      {/* Backdrop */}
      <div 
        className={`fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-[60] transition-opacity duration-300 ${
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onClose}
      />

      {/* Drawer */}
      <div 
        className={`fixed inset-y-0 right-0 w-full sm:w-96 bg-slate-900 border-l border-slate-800 shadow-2xl z-[70] transform transition-transform duration-300 ease-out ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-indigo-400" />
              <h2 className="text-lg font-semibold text-slate-100">Session History</h2>
            </div>
            <button 
              onClick={onClose}
              className="p-2 rounded-full hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* List */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {sessions.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-48 text-slate-500 space-y-2">
                <Clock className="w-10 h-10 opacity-20" />
                <p className="text-sm">No archived sessions found.</p>
              </div>
            ) : (
              sessions.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()).map((session) => (
                <div 
                  key={session.id}
                  className="bg-slate-800/30 border border-slate-800 rounded-xl p-4 hover:border-indigo-500/30 transition-all group"
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="text-sm font-medium text-slate-200 line-clamp-1">{session.title}</h3>
                      <p className="text-xs text-slate-500 font-mono mt-0.5">
                        {new Date(session.date).toLocaleDateString()} • {new Date(session.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </p>
                    </div>
                    <button 
                      onClick={(e) => { e.stopPropagation(); onDelete(session.id); }}
                      className="text-slate-600 hover:text-red-400 p-1 rounded transition-colors"
                      title="Delete Session"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                  
                  <div className="flex items-center gap-3 mb-4">
                     <div className="flex items-center gap-1.5 text-[10px] text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-800">
                        <FileText className="w-3 h-3" />
                        <span className="truncate max-w-[120px]">{session.fileName}</span>
                     </div>
                     <div className="flex items-center gap-1.5 text-[10px] text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-800">
                        <span>{session.messages.length} msgs</span>
                     </div>
                  </div>

                  <button 
                    onClick={() => { onRestore(session); onClose(); }}
                    className="w-full flex items-center justify-center gap-2 bg-indigo-600/10 hover:bg-indigo-600/20 text-indigo-300 text-xs font-medium py-2 rounded-lg border border-indigo-500/20 transition-colors"
                  >
                    <ArrowRightCircle className="w-3.5 h-3.5" />
                    Restore Session
                  </button>
                </div>
              ))
            )}
          </div>
          
          <div className="p-4 border-t border-slate-800 bg-slate-950/50 text-center">
             <p className="text-[10px] text-slate-500">History is saved locally in your browser.</p>
          </div>
        </div>
      </div>
    </>
  );
};
