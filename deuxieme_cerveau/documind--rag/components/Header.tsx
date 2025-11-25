
import React from 'react';
import { FileText, Layers, BrainCircuit, History } from 'lucide-react';

interface HeaderProps {
  onToggleHistory: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleHistory }) => {
  return (
    <header className="bg-slate-950/80 backdrop-blur-md border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-br from-indigo-600 to-violet-600 p-2 rounded-xl shadow-lg shadow-indigo-500/20">
            <BrainCircuit className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-slate-100 tracking-tight">
            Docu<span className="text-indigo-400">Mind</span>
          </span>
        </div>
        <div className="flex items-center space-x-3 text-xs sm:text-sm">
          
          <div className="hidden sm:flex items-center space-x-2 text-slate-400 px-3 py-1.5 rounded-full border border-slate-800 bg-slate-900/50">
            <Layers className="w-3.5 h-3.5 text-indigo-400" />
            <span className="font-medium">Orchestrator V2</span>
          </div>

          <button 
            onClick={onToggleHistory}
            className="flex items-center space-x-2 text-slate-400 px-3 py-1.5 rounded-full border border-slate-800 bg-slate-900/50 hover:bg-slate-800 hover:text-indigo-300 transition-all cursor-pointer"
          >
            <History className="w-3.5 h-3.5" />
            <span className="font-medium hidden sm:inline">History</span>
          </button>

          <div className="flex items-center space-x-2 text-slate-400 px-3 py-1.5 rounded-full border border-slate-800 bg-slate-900/50">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="font-medium">Gemini 2.5 Flash</span>
          </div>
        </div>
      </div>
    </header>
  );
};
