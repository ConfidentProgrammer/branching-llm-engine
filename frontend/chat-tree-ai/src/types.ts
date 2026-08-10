export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
}

export interface ChatNodeData {
  nodeId: string;
  title: string;
  messages: ChatMessage[];
  onAddMessage: (nodeId: string, text: string) => void;
  onBranch: (nodeId: string) => void;
  [key: string]: unknown;
}