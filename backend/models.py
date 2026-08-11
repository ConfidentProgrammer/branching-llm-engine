from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, text
from pgvector.sqlalchemy import Vector
from database import Base

class Node(Base):
    __tablename__ = "nodes"
    
    # We use String(50) to store our UUIDs
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    
    # Self-referential foreign key for the tree structure
    parent_id = Column(String(50), ForeignKey("nodes.id", ondelete="CASCADE"), nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(20), nullable=False) # 'user' or 'assistant'
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

class NodeEmbedding(Base):
    __tablename__ = "node_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), ForeignKey("nodes.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # We define the Vector dimension as 768 for text-embedding-004.
    # Note: If you ever switch to a model with different dimensions, 
    # you update this number here.
    embedding = Column(Vector(1536))