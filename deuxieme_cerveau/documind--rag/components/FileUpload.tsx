import React, { useCallback, useState } from 'react';
import { UploadCloud, FileText, Loader2, AlertCircle, FileCode, FileJson } from 'lucide-react';
import { UploadedFile } from '../types';

interface FileUploadProps {
  onFileUpload: (file: UploadedFile) => void;
}

const SUPPORTED_EXTENSIONS = [
  '.pdf', 
  '.txt', '.md', '.markdown', 
  '.json', '.csv', '.xml', '.yaml', '.yml',
  '.py', '.js', '.jsx', '.ts', '.tsx', 
  '.html', '.css', '.scss',
  '.java', '.c', '.cpp', '.h', '.cs', 
  '.rb', '.php', '.go', '.rs', '.swift',
  '.sql', '.sh', '.bat', '.ini', '.config'
];

export const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateFile = (file: File): string | null => {
    if (file.size > 20 * 1024 * 1024) { // 20MB limit
      return 'File size too large. Please upload a file smaller than 20MB.';
    }

    const fileName = file.name.toLowerCase();
    const isValidExtension = SUPPORTED_EXTENSIONS.some(ext => fileName.endsWith(ext));
    const isTextMime = file.type.startsWith('text/');

    if (!isValidExtension && !isTextMime) {
      return 'Unsupported file type. Please upload a PDF or text-based document.';
    }
    return null;
  };

  const processFile = (file: File) => {
    setError(null);
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsProcessing(true);
    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      const base64Data = result.split(',')[1];
      
      onFileUpload({
        name: file.name,
        type: file.type || 'application/octet-stream',
        size: file.size,
        base64Data: base64Data
      });
      setIsProcessing(false);
    };
    reader.onerror = () => {
      setError('Failed to read file.');
      setIsProcessing(false);
    };
    reader.readAsDataURL(file);
  };

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  }, []);

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <div 
        className={`relative border-2 border-dashed rounded-3xl p-12 transition-all duration-300 ease-out text-center cursor-pointer group overflow-hidden
          ${isDragging 
            ? 'border-indigo-500 bg-indigo-500/10 scale-[1.02] shadow-xl shadow-indigo-500/20' 
            : 'border-slate-700 hover:border-indigo-400 hover:bg-slate-800/50'
          }`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => document.getElementById('fileInput')?.click()}
      >
        <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/5 via-transparent to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
        
        <input 
          type="file" 
          id="fileInput" 
          accept={SUPPORTED_EXTENSIONS.join(',') + ',text/*'}
          className="hidden" 
          onChange={onFileChange}
        />
        
        <div className="flex flex-col items-center justify-center space-y-6 relative z-10">
          <div className={`p-5 rounded-2xl ${isDragging ? 'bg-indigo-500/20' : 'bg-slate-800 group-hover:bg-slate-700'} transition-colors shadow-lg`}>
            {isProcessing ? (
              <Loader2 className="w-10 h-10 text-indigo-400 animate-spin" />
            ) : (
              <UploadCloud className={`w-10 h-10 ${isDragging ? 'text-indigo-400' : 'text-slate-400 group-hover:text-indigo-400'}`} />
            )}
          </div>
          
          <div className="space-y-2">
            <h3 className="text-xl font-bold text-slate-200 group-hover:text-white transition-colors">
              {isProcessing ? 'Processing Document...' : 'Upload Knowledge Source'}
            </h3>
            <p className="text-sm text-slate-400 max-w-xs mx-auto">
              Drag & drop or click to browse.
            </p>
          </div>
          
          <div className="flex flex-wrap justify-center gap-2 mt-2">
            <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-500 font-mono border border-slate-700">PDF</span>
            <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-500 font-mono border border-slate-700">JSON</span>
            <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-500 font-mono border border-slate-700">CODE</span>
            <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-500 font-mono border border-slate-700">TXT</span>
          </div>
        </div>
      </div>

      {error && (
        <div className="mt-6 p-4 bg-red-900/20 border border-red-500/30 text-red-400 text-sm rounded-xl flex items-center justify-center animate-in fade-in slide-in-from-top-2">
          <AlertCircle className="w-4 h-4 mr-2" />
          {error}
        </div>
      )}
    </div>
  );
};