import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, AlertTriangle, BrainCircuit, ChevronDown, ChevronRight } from 'lucide-react';
import { Message, MessageRole } from '../types';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === MessageRole.USER;
  const isError = message.isError;
  const hasThoughts = message.thinkingLogs && message.thinkingLogs.length > 0;

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-8 animate-in slide-in-from-bottom-2 duration-300`}>
      <div className={`flex max-w-[90%] sm:max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-3`}>
        
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center mt-1 border
          ${isUser ? 'bg-indigo-600 border-indigo-500 shadow-lg shadow-indigo-500/20' : isError ? 'bg-red-500/10 border-red-500/20' : 'bg-slate-800 border-slate-700'}`}>
          {isUser ? (
            <User className="w-4 h-4 text-white" />
          ) : isError ? (
            <AlertTriangle className="w-4 h-4 text-red-400" />
          ) : (
            <Bot className="w-4 h-4 text-indigo-400" />
          )}
        </div>

        {/* Bubble */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} w-full`}>
          
          {/* Thinking Process Dropdown (Only for Bot) */}
          {!isUser && hasThoughts && (
             <details className="mb-3 w-full max-w-2xl group/details">
              <summary className="list-none flex items-center gap-2 text-xs font-mono text-slate-500 cursor-pointer hover:text-indigo-400 transition-colors select-none py-1">
                <BrainCircuit className="w-3 h-3" />
                <span>Process Log ({message.thinkingLogs!.length} ops)</span>
                <ChevronRight className="w-3 h-3 group-open/details:rotate-90 transition-transform" />
              </summary>
              <div className="mt-2 p-3 bg-slate-950/50 rounded-lg border border-slate-800 text-[10px] sm:text-xs font-mono text-slate-400 space-y-1.5 animate-in slide-in-from-top-1 overflow-x-auto">
                {message.thinkingLogs!.map((log, i) => (
                  <div key={i} className="flex items-start gap-2 border-l-2 border-slate-800 pl-2 hover:border-indigo-500/50 transition-colors">
                    <span className="text-slate-600 select-none">{(i + 1).toString().padStart(2, '0')}</span>
                    <span className="leading-relaxed">{log}</span>
                  </div>
                ))}
              </div>
            </details>
          )}

          <div className={`px-5 py-4 rounded-2xl shadow-sm text-sm sm:text-base leading-relaxed w-full border
            ${isUser 
              ? 'bg-indigo-600/90 backdrop-blur text-white border-indigo-500/50 rounded-tr-sm' 
              : isError
                ? 'bg-red-900/20 text-red-200 border-red-500/20 rounded-tl-sm'
                : 'bg-slate-900 text-slate-200 border-slate-800 rounded-tl-sm shadow-xl'
            }`}>
            {isError ? (
              <p>{message.content}</p>
            ) : (
              <div className={`markdown-content prose prose-sm max-w-none ${isUser ? 'prose-invert' : 'prose-invert prose-p:text-slate-300 prose-headings:text-slate-100 prose-strong:text-white prose-code:text-indigo-300'}`}>
                <ReactMarkdown
                  components={{
                    p: ({children}) => <p className="mb-4 last:mb-0 leading-7">{children}</p>,
                    h1: ({children}) => <h1 className="text-xl font-bold mb-4 mt-6 pb-2 border-b border-slate-800">{children}</h1>,
                    h2: ({children}) => <h2 className="text-lg font-bold mb-3 mt-6 text-indigo-200">{children}</h2>,
                    h3: ({children}) => <h3 className="text-md font-bold mb-2 mt-4 text-indigo-300">{children}</h3>,
                    ul: ({children}) => <ul className="list-disc pl-4 mb-4 space-y-2 marker:text-slate-500">{children}</ul>,
                    ol: ({children}) => <ol className="list-decimal pl-4 mb-4 space-y-2 marker:text-slate-500">{children}</ol>,
                    blockquote: ({children}) => <blockquote className="border-l-4 border-indigo-500/50 pl-4 italic my-4 text-slate-400 bg-slate-950/30 py-2 rounded-r pr-2">{children}</blockquote>,
                    code: ({node, inline, className, children, ...props}: any) => {
                       return inline ? (
                        <code className={`${isUser ? 'bg-indigo-700/50 text-indigo-100' : 'bg-slate-950 text-indigo-300 border border-slate-800'} px-1.5 py-0.5 rounded text-xs font-mono`} {...props}>
                          {children}
                        </code>
                      ) : (
                        <code className="block bg-slate-950 text-slate-300 p-4 rounded-lg text-xs overflow-x-auto my-4 font-mono border border-slate-800 shadow-inner" {...props}>
                          {children}
                        </code>
                      )
                    }
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>
          
          {/* Timestamp */}
          <span className={`text-[10px] text-slate-600 mt-1.5 px-1 opacity-0 group-hover:opacity-100 transition-opacity`}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      </div>
    </div>
  );
};