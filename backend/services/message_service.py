from datetime import UTC, datetime
import select
import uuid

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
from models import Message, NodeEmbedding # Ensure MessageEmbedding model exists
from schemas import MessageCreateRequest
from services.ai_service import ai_client

logger = logging.getLogger(__name__)

class MessageService:

    @staticmethod
    def generate_embedding(text: str) -> list[float]:
        try:
            response = ai_client.models.embed_content(
                model="gemini-embedding-2",
                contents=text,
                config={"output_dimensionality": 1536}
            )
            return response.embeddings[0].values
        except Exception as e:
            logger.error(f"Embedding API error: {str(e)}")
            raise Exception("AI Embedding Generation failed")

        

    @classmethod
    def create_message_with_embedding(cls, db: Session, node_id: str, payload: MessageCreateRequest) -> Message:
        """
        Saves the message to DB and creates its vector embedding atomically.
        """
        try:
            # 1. Create and save the message
            new_message = Message(
                id=payload.id,
                node_id=node_id,
                sender=payload.sender,
                content=payload.content,
                created_at=datetime.now(UTC)
            )
            db.add(new_message)
            
            # 2. Generate embedding for the message content
            # Using the embedding service we discussed
            embedding_vector = cls.generate_embedding(payload.content)
            
            # 3. Save the embedding linked to this message ID
            new_embedding = NodeEmbedding(
                id=str(uuid.uuid4()),
                node_id=node_id,
                embedding=embedding_vector
            )
            db.add(new_embedding)
            
            # 4. Atomic Commit
            db.commit()
            db.refresh(new_message)
            db.refresh(new_embedding)
            
            logger.info(f"Message {new_message.id} saved with embedding.")
            return new_message

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save message and embedding: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Transaction failed: Could not save message or embedding."
            )

    @classmethod
    def get_global_top_k_messages(cls, db: Session, query_vector: list[float], k: int = 5) -> list[NodeEmbedding]:
        """
        Performs a vector similarity search using pgvector cosine distance.
        """
        try:
            # Query the NodeEmbedding table ordered by cosine distance
            statement = (
                select(Message)
                .join(NodeEmbedding, Message.node_id == NodeEmbedding.node_id)
                .order_by(NodeEmbedding.embedding.cosine_distance(query_vector))
                .limit(k)
            )
            results = db.scalars(statement).all()
            return results
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            return []
