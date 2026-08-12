import uuid

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
from services.ai_service import ai_client
from models import Node, NodeEmbedding
from schemas import NodeCreateRequest

logger = logging.getLogger(__name__)

class NodeService:
    
    @classmethod
    def create_node(cls, db: Session, payload: NodeCreateRequest) -> Node:
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
                id=str(uuid.uuid4()),
                title=payload.title,
                parent_id=payload.parent_id
            )
            db.add(new_node)

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