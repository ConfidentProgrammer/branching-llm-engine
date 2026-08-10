import React, { useState, useCallback } from 'react';
import { 
  ReactFlow, 
  Background, 
  Controls, 
  addEdge, 
  useNodesState, 
  useEdgesState, 
  type Connection,
  type Edge
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { ChatNode } from './components/ChatNode';
import type { ChatNodeData, ChatMessage } from './types';
import { Layers, MessageSquare, Plus, ChevronLeft, ChevronRight, Sparkles } from 'lucide-react';

const nodeTypes = {
  chatNode: ChatNode,
};

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Handlers declaration hoisted for initial nodes setup
  const handleAddMessage = (nodeId: string, text: string) => {
    console.log('inside handle add message')
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId || node.data.nodeId === nodeId) {
          const newMessage: ChatMessage = {
            id: Date.now().toString(),
            sender: 'user',
            text,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          };
          
          // Simulate AI response toggle
          const aiResponse: ChatMessage = {
            id: (Date.now() + 1).toString(),
            sender: 'assistant',
            text: `Processed vector query context for branch: "${text.slice(0, 20)}..."`,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          };

          return {
            ...node,
            data: {
              ...node.data,
              messages: [...(node.data.messages as ChatMessage[]), newMessage, aiResponse],
            },
          };
        }
        return node;
      })
    );
  };

  const handleBranchCreation = useCallback((parentId: string) => {
    const newId = `node_${Date.now().toString().slice(-4)}`;
    
    setNodes((nds) => {
      const parentNode = nds.find((n) => n.id === parentId || n.data.nodeId === parentId);
      const posX = parentNode ? parentNode.position.x + 340 : 100;
      const posY = parentNode ? parentNode.position.y + 120 : 100;

      const newNode = {
        id: newId,
        type: 'chatNode',
        position: { x: posX, y: posY },
        data: {
          nodeId: newId,
          title: `Branch / ${newId}`,
          messages: [
            {
              id: '1',
              sender: 'assistant' as const,
              text: 'New conversation thread branched successfully. Ready for prompt input.',
              timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            }
          ],
          onAddMessage: handleAddMessage,
          onBranch: handleBranchCreation,
        } as ChatNodeData,
      };

      return [...nds, newNode];
    });

    setEdges((eds) => [
      ...eds,
      {
        id: `e-${parentId}-${newId}`,
        source: parentId,
        target: newId,
        type: 'simplebezier',
        style: { stroke: '#3f3f46', strokeWidth: 1.5 },
      } as Edge,
    ]);
  }, []);

  const initialNodes = [
    {
      id: 'node-root',
      type: 'chatNode',
      position: { x: 100, y: 150 },
      data: {
        nodeId: 'node-root',
        title: 'Main Pipeline / Root',
        messages: [
          {
            id: '1',
            sender: 'user' as const,
            text: 'How do I optimize pgvector index lookups in FastAPI?',
            timestamp: '10:42 AM',
          },
          {
            id: '2',
            sender: 'assistant' as const,
            text: 'You can configure HNSW parameters and ensure your distance metrics match your query embeddings.',
            timestamp: '10:42 AM',
          },
        ],
        onAddMessage: handleAddMessage,
        onBranch: handleBranchCreation,
      } as ChatNodeData,
    },
  ];

  const initialEdges: Edge[] = [];

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge({ ...params, type: 'simplebezier', style: { stroke: '#3f3f46', strokeWidth: 1.5 } }, eds)),
    [setEdges]
  );

  return (
    <div className="w-screen h-screen flex bg-[#090a0f] text-zinc-100 font-sans overflow-hidden select-none">
      
      {/* Collapsible Minimal Workspace Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-16'} bg-[#0d0e12] border-r border-zinc-800/80 flex flex-col justify-between transition-all duration-200 z-20`}>
        <div>
          {/* Sidebar Header */}
          <div className="h-14 px-4 border-b border-zinc-800/80 flex items-center justify-between">
            {sidebarOpen && (
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded bg-indigo-600 flex items-center justify-center text-white font-bold text-xs">
                  C
                </div>
                <span className="font-semibold text-xs tracking-tight text-zinc-200">ChatTree Workspace</span>
              </div>
            )}
            <button 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-1.5 rounded text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50 transition-colors ml-auto"
            >
              {sidebarOpen ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
            </button>
          </div>

          {/* Navigation Items */}
          <div className="p-3 space-y-1">
            <div className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider px-2 py-1">
              {sidebarOpen && 'Workspaces'}
            </div>
            <button className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-md bg-zinc-800/60 text-zinc-200 text-xs font-medium">
              <Layers size={14} className="text-indigo-400" />
              {sidebarOpen && <span>Default Project</span>}
            </button>
            <button className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-md hover:bg-zinc-800/30 text-zinc-400 hover:text-zinc-200 text-xs font-medium transition-colors">
              <MessageSquare size={14} />
              {sidebarOpen && <span>RAG Optimization Tree</span>}
            </button>
          </div>
        </div>

        {/* Sidebar Footer status */}
        {sidebarOpen && (
          <div className="p-3 m-3 bg-[#121316] border border-zinc-800 rounded-lg text-[11px] text-zinc-400 space-y-1">
            <div className="flex items-center justify-between font-medium text-zinc-300">
              <span>Engine Status</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            </div>
            <p className="text-[10px] text-zinc-500">pgvector metadata isolation ready.</p>
          </div>
        )}
      </aside>

      {/* Main Canvas Workspace */}
      <main className="flex-1 h-full relative bg-canvas-dark">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background gap={32} size={1} color="#1f2430" />
          <Controls className="!bg-[#121316] !border !border-zinc-800 !rounded-lg !shadow-xl overflow-hidden [&>button]:!border-b [&>button]:!border-zinc-800 [&>button]:!bg-[#121316] [&>button:hover]:!bg-zinc-800 [&>button]:!fill-zinc-300" />
        </ReactFlow>
      </main>

    </div>
  );
}