
import React, { useRef, useEffect, useState } from 'react';
import { Send, FileText, Trash2, Bot, Loader2, Sparkles, Command, Zap, Brain, Banknote, Lock } from 'lucide-react';
import { Message, UploadedFile, ThinkingState, WorkflowStage } from '../types';
import { MessageBubble } from './MessageBubble';
import { ThinkingProcess } from './ThinkingProcess';

interface ChatInterfaceProps {
  messages: Message[];
  file: UploadedFile;
  isLoading: boolean;
  thinkingState: ThinkingState | null;
  workflowStage: WorkflowStage;
  onSendMessage: (text: string) => void;
  onClearChat: () => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
  messages, 
  file, 
  isLoading,
  thinkingState,
  workflowStage,
  onSendMessage,
  onClearChat 
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, thinkingState?.currentStreamText]);

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] sm:h-[calc(100vh-140px)] bg-slate-900">
      
      {/* File Info Banner */}
      <div className="bg-slate-900/90 border-b border-slate-800 px-6 py-3 flex items-center justify-between backdrop-blur-sm z-20">
        <div className="flex items-center space-x-3 overflow-hidden">
          <div className="bg-indigo-500/10 p-2 rounded-lg border border-indigo-500/20">
            <FileText className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="flex flex-col overflow-hidden">
            <h2 className="text-sm font-semibold text-slate-200 truncate max-w-[200px]">{file.name}</h2>
            <p className="text-[10px] text-slate-500 uppercase tracking-wider font-mono">{(file.size / 1024 / 1024).toFixed(2)} MB • {file.type.split('/')[1] || 'doc'}</p>
          </div>
        </div>
        <button 
          onClick={onClearChat}
          className="text-slate-500 hover:text-red-400 transition-colors p-2 rounded-lg hover:bg-red-500/10 flex items-center gap-2 group"
          title="Eject Document"
        >
          <span className="text-xs font-medium hidden group-hover:block">Eject</span>
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 scrollbar-hide bg-slate-950/30">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center opacity-0 animate-in fade-in duration-700" style={{animationFillMode: 'forwards'}}>
            <div className="w-20 h-20 bg-slate-900 rounded-3xl flex items-center justify-center shadow-2xl shadow-indigo-500/10 mb-8 border border-slate-800 relative">
               <div className="absolute inset-0 bg-indigo-500/20 blur-xl rounded-full opacity-20"></div>
              <Bot className="w-10 h-10 text-indigo-400 relative z-10" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Deep Reasoning Engine</h3>
            <p className="text-slate-400 max-w-md leading-relaxed mb-10 text-sm">
              Ready to analyze <span className="font-semibold text-indigo-300">{file.name}</span>.
              <br/>
              <span className="text-slate-600 mt-2 block">Initiate the 3-Stage Expert Workflow below.</span>
            </p>
          </div>
        ) : (
          <div className="space-y-8 max-w-3xl mx-auto">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
          </div>
        )}
        
        {/* Active Thinking Process Display */}
        {isLoading && thinkingState && (
          <div className="mb-8 max-w-4xl mx-auto">
             <ThinkingProcess state={thinkingState} />
          </div>
        )}

        <div ref={messagesEndRef} className="h-4" />
      </div>

      {/* 3-Button Control Deck */}
      <div className="bg-slate-900 border-t border-slate-800 p-4 sm:px-6 sm:py-6">
        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4">
          
          {/* Button 1: ANALYSE */}
          <button
            onClick={() => onSendMessage("STAGE_1")}
            disabled={workflowStage !== WorkflowStage.IDLE || isLoading}
            className={`relative group p-4 rounded-xl border transition-all duration-300 flex flex-col items-center justify-center gap-2
              ${workflowStage === WorkflowStage.IDLE 
                ? 'bg-slate-800/50 border-indigo-500/50 hover:bg-indigo-500/10 hover:border-indigo-400 cursor-pointer shadow-lg shadow-indigo-900/10' 
                : workflowStage > WorkflowStage.IDLE 
                  ? 'bg-slate-900 border-slate-800 opacity-50 cursor-not-allowed'
                  : 'bg-slate-900 border-slate-800 opacity-50 cursor-not-allowed'
              }
            `}
          >
            {workflowStage === WorkflowStage.IDLE && !isLoading && (
              <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-blue-500 rounded-xl opacity-20 group-hover:opacity-40 blur transition duration-500"></div>
            )}
            <div className="relative flex flex-col items-center">
               <Zap className={`w-6 h-6 mb-2 ${workflowStage === WorkflowStage.IDLE ? 'text-indigo-400' : 'text-slate-600'}`} />
               <span className={`font-bold text-sm ${workflowStage === WorkflowStage.IDLE ? 'text-indigo-100' : 'text-slate-500'}`}>1. Analyse</span>
               <span className="text-[10px] text-slate-500">Structure & Decompose</span>
            </div>
          </button>

          {/* Button 2: MAKE IT SMART */}
          <button
            onClick={() => onSendMessage("STAGE_2")}
            disabled={workflowStage < WorkflowStage.ANALYSIS_COMPLETE || workflowStage >= WorkflowStage.SMART_ENRICHING || isLoading}
            className={`relative group p-4 rounded-xl border transition-all duration-300 flex flex-col items-center justify-center gap-2
              ${workflowStage === WorkflowStage.ANALYSIS_COMPLETE
                ? 'bg-slate-800/50 border-purple-500/50 hover:bg-purple-500/10 hover:border-purple-400 cursor-pointer shadow-lg shadow-purple-900/10'
                : 'bg-slate-900 border-slate-800 opacity-40 cursor-not-allowed'
              }
            `}
          >
             {workflowStage === WorkflowStage.ANALYSIS_COMPLETE && !isLoading && (
              <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl opacity-20 group-hover:opacity-40 blur transition duration-500"></div>
            )}
             <div className="relative flex flex-col items-center">
               {workflowStage < WorkflowStage.ANALYSIS_COMPLETE ? (
                 <Lock className="w-6 h-6 mb-2 text-slate-700" />
               ) : (
                 <Brain className={`w-6 h-6 mb-2 ${workflowStage === WorkflowStage.ANALYSIS_COMPLETE ? 'text-purple-400' : 'text-slate-600'}`} />
               )}
               <span className={`font-bold text-sm ${workflowStage === WorkflowStage.ANALYSIS_COMPLETE ? 'text-purple-100' : 'text-slate-600'}`}>2. Make it Smart</span>
               <span className="text-[10px] text-slate-500">5-Level Strategic Reasoning</span>
            </div>
          </button>

          {/* Button 3: INSANITY */}
          <button
            onClick={() => onSendMessage("STAGE_3")}
            disabled={workflowStage < WorkflowStage.SMART_COMPLETE || workflowStage === WorkflowStage.INSANITY_COMPLETE || isLoading}
            className={`relative group p-4 rounded-xl border transition-all duration-300 flex flex-col items-center justify-center gap-2
              ${workflowStage === WorkflowStage.SMART_COMPLETE
                ? 'bg-slate-800/50 border-emerald-500/50 hover:bg-emerald-500/10 hover:border-emerald-400 cursor-pointer shadow-lg shadow-emerald-900/10'
                : 'bg-slate-900 border-slate-800 opacity-40 cursor-not-allowed'
              }
            `}
          >
             {workflowStage === WorkflowStage.SMART_COMPLETE && !isLoading && (
              <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500 to-amber-500 rounded-xl opacity-20 group-hover:opacity-40 blur transition duration-500"></div>
            )}
             <div className="relative flex flex-col items-center">
               {workflowStage < WorkflowStage.SMART_COMPLETE ? (
                 <Lock className="w-6 h-6 mb-2 text-slate-700" />
               ) : (
                 <Banknote className={`w-6 h-6 mb-2 ${workflowStage === WorkflowStage.SMART_COMPLETE ? 'text-emerald-400' : 'text-slate-600'}`} />
               )}
               <span className={`font-bold text-sm ${workflowStage === WorkflowStage.SMART_COMPLETE ? 'text-emerald-100' : 'text-slate-600'}`}>3. Insanity</span>
               <span className="text-[10px] text-slate-500">Maximize Value & Impact</span>
            </div>
          </button>

        </div>
        
        <div className="flex justify-center items-center space-x-4 mt-4 opacity-50">
             <p className="text-[10px] text-slate-600 font-mono flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                Gemini 2.5 Flash
             </p>
             <p className="text-[10px] text-slate-600 font-mono flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-purple-500"></span>
                Gemini 3 Pro
             </p>
        </div>
      </div>
    </div>
  );
};
