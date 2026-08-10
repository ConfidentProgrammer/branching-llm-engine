-- 1. Enable the pgvector extension (Must be done per database)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Nodes Table (Tracks tree topology and ancestry)
CREATE TABLE IF NOT EXISTS nodes (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    parent_id VARCHAR(50) REFERENCES nodes(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Messages Table (Individual chat items linked to a specific node)
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(50) REFERENCES nodes(id) ON DELETE CASCADE,
    sender VARCHAR(20) CHECK (sender IN ('user', 'assistant')) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Node Embeddings Table (For pgvector semantic RAG lookups)
-- Industry standard dimension size for text-embedding-3-small is 1536
CREATE TABLE IF NOT EXISTS node_embeddings (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(50) REFERENCES nodes(id) ON DELETE CASCADE,
    embedding VECTOR(1536), 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create an HNSW index for lightning-fast approximate nearest neighbor (ANN) vector searches
CREATE INDEX IF NOT EXISTS node_embeddings_hnsw_idx 
ON node_embeddings 
USING hnsw (embedding vector_cosine_ops);