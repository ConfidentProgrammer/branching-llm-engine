import uuid
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import Message
from schemas import MessageCreateRequest
from services.message_service import MessageService
from services.ai_service import ai_client

logger = logging.getLogger(__name__)


class ChatOrchestrationService:

    @classmethod
    def process_chat(cls, db: Session, node_id: str, user_content: str) -> Message:
        """
        Orchestrates the entire chat loop:
        1. Save user query + vector embedding
        2. Perform global top 10 vector similarity search
        3. Build prompt and call LLM
        4. Save AI response + vector embedding atomically
        """
        try:
            # ---------------------------------------------------------
            # STEP 1: Save User Message & Generate Vector Atomically
            # ---------------------------------------------------------
            user_msg_req = MessageCreateRequest(
                id=str(uuid.uuid4()), 
                sender="user", 
                content=user_content
            )
            MessageService.create_message_with_embedding(db, node_id, user_msg_req)

            # ---------------------------------------------------------
            # STEP 2: Global Vector Search (Top 10 Across All Nodes)
            # ---------------------------------------------------------
            query_vector = MessageService.generate_embedding(user_content)
            
            matching_messages = MessageService.get_global_top_k_messages(db, query_vector, k=10)
            
            context_texts = [msg.content for msg in matching_messages]
            context_block = "\n---\n".join(context_texts)

            # ---------------------------------------------------------
            # STEP 3: Prompt the LLM
            # ---------------------------------------------------------
            system_prompt = (
                "You are an AI assistant in a tree-based chat architecture. "
                "Use the following global context snippets if relevant to answer the query:\n\n"
                f"{context_block}"
            )

            response = ai_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[system_prompt, f"User Query: {user_content}"]
            )
            ai_response_text = response.text

            # ---------------------------------------------------------
            # STEP 4: Save AI Response & Vector Atomically
            # ---------------------------------------------------------
            ai_msg_req = MessageCreateRequest(
                id=str(uuid.uuid4()), 
                sender="ai", 
                content=ai_response_text
            )
            saved_ai_msg = MessageService.create_message_with_embedding(db, node_id, ai_msg_req)

            return saved_ai_msg

        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Chat Orchestration failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Chat orchestration error: {str(e)}"
            )