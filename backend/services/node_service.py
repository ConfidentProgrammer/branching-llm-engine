from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from models import Node, NodeEmbedding
from schemas import NodeCreateRequest

logger = logging.getLogger(__name__)

class NodeService:
    @staticmethod
    def generate_embedding(text: str) -> list[float]:
        """
        Placeholder / Integration point for generating vector embeddings.
        Must return a 1536-dimensional list of floats to match pgvector(1536).
        """
        # TODO: Replace with actual embedding call (e.g., OpenAI API, HuggingFace, etc.)
        # Returning a dummy 1536-dim vector of zeros for architectural wiring verification
        return [0.0] * 1536

    @classmethod
    def create_node_with_embedding(cls, db: Session, payload: NodeCreateRequest) -> Node:
        """
        Fails fast if parent doesn't exist, creates the node, 
        generates its embedding, and saves it to PostgreSQL atomically.
        """
        try:
            # 1. If a parent_id is provided, verify it exists (Fail Fast)
            if payload.parent_id:
                parent_node = db.query(Node).filter(Node.id == payload.parent_id).first()
                if not parent_node:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Parent node with ID '{payload.parent_id}' does not exist."
                    )

            # 2. Create the Node record
            new_node = Node(
                id=payload.id,
                title=payload.title,
                parent_id=payload.parent_id
            )
            db.add(new_node)

            # 3. Generate vector embedding from text content
            vector_data = cls.generate_embedding(payload.content)

            # 4. Create the Vector Embedding record linked to the node
            new_embedding = NodeEmbedding(
                node_id=new_node.id,
                embedding=vector_data
            )
            db.add(new_embedding)

            # 5. Commit transaction atomically (All or nothing)
            db.commit()
            db.refresh(new_node)
            
            logger.info(f"Successfully created node {new_node.id} with vector embedding.")
            return new_node

        except HTTPException as he:
            db.rollback()
            raise he
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create node and embedding: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database transaction error: {str(e)}"
            )