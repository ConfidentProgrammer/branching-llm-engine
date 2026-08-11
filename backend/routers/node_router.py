from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import NodeCreateRequest, NodeResponse
from services.node_service import NodeService

router = APIRouter(prefix="/nodes", tags=["Chat Nodes"])

@router.post("/", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
def create_node(payload: NodeCreateRequest, db: Session = Depends(get_db)):
    """
    Endpoint to create a new structural chat tree node (branch).
    """
    return NodeService.create_node(db, payload)