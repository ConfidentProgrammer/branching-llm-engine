import React, { useState,  useRef, useEffect } from 'react';
import { Handle, Position } from '@xyflow/react';
import type { ChatNodeData } from '../types';
import { Send, GitBranch, Sparkles } from 'lucide-react';

interface ChatNodeProps {
  data: ChatNodeData;
}

export const ChatNode: React.FC<ChatNodeProps> = ({ data }) => {
  const [inputText, setInputText] = useState('');

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [data.messages])
  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    data.onAddMessage(data.nodeId, inputText);
    setInputText('');
  };

  return (
    <div className="w-90 h-100 bg-[#121316] text-zinc-200 border border-zinc-800 rounded-lg shadow-2xl flex flex-col font-sans overflow-hidden transition-all">
      {/* Top Handle for Parent Connection */}
      <Handle 
        type="target" 
        position={Position.Top} 
        className="w-2.5 h-2.5 !bg-zinc-600 !border-none !rounded-full" 
      />

      {/* Node Header */}
      <div className="px-4 py-3 bg-[#18191e] border-b border-zinc-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-5 h-5 rounded bg-indigo-600/20 text-indigo-400 flex items-center justify-center text-[10px] font-bold border border-indigo-500/30">
            AI
          </div>
          <span className="text-xs font-semibold tracking-wide text-zinc-300">{data.title}</span>
        </div>
        <span className="flex items-center gap-1.5 text-[10px] text-zinc-400 font-medium">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          active
        </span>
      </div>

      {/* Internal Chat Message Stream */}
      <div className="p-3 max-h-56 overflow-y-auto space-y-3 text-xs bg-[#121316] nowheel "
      onPointerDown={(e) => e.stopPropagation()}>
        {data.messages.map((msg) => (
          <div 
            key={msg.id} 
            className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div className="flex items-center gap-1.5 text-[10px] text-zinc-500 px-1">
              <span>{msg.sender === 'user' ? 'You' : 'Assistant'}</span>
              <span>•</span>
              <span>{msg.timestamp}</span>
            </div>
            <div 
              className={`p-2.5 rounded-md leading-relaxed max-w-[90%] ${
                msg.sender === 'user' 
                  ? 'bg-indigo-600 text-white font-normal' 
                  : 'bg-[#1a1b20] text-zinc-300 border border-zinc-800/80'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Node Footer Actions & Input */}
      <div className="p-3 bg-[#16171c] border-t border-zinc-800 flex flex-col gap-2">
        <form onSubmit={handleSend} className="flex items-center gap-1.5 bg-[#101114] border border-zinc-800 rounded-md px-2.5 py-1 focus-within:border-indigo-500 transition-colors">
          <input 
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Reply in node..."
            className="w-full bg-transparent text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none py-1"
          />
          <button type="submit" className="text-zinc-400 hover:text-indigo-400 transition-colors">
            <Send size={12} />
          </button>
        </form>

        <button 
          onClick={() => data.onBranch(data.nodeId)}
          className="w-full py-1.5 px-2 bg-transparent hover:bg-zinc-800/50 text-zinc-400 hover:text-zinc-200 border border-zinc-800 rounded-md text-[11px] font-medium flex items-center justify-center gap-1.5 transition-all"
        >
          <GitBranch size={12} className="text-indigo-400" />
          <span>Branch Conversation</span>
        </button>
      </div>

      {/* Bottom Handle for Child Connections */}
      <Handle 
        type="source" 
        position={Position.Bottom} 
        className="w-2.5 h-2.5 !bg-zinc-600 !border-none !rounded-full" 
      />
    </div>
  );
};