import uuid

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DBStatusResponse(BaseModel):
    status: str
    message: str
    test_query_result: Optional[int] = None
    timestamp: datetime

class NodeCreateRequest(BaseModel):
    title: str = Field(..., max_length=255)
    parent_id: Optional[str] = Field(None, description="Parent node ID if this is a branch")

class NodeResponse(BaseModel):
    id: str
    title: str
    parent_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class MessageCreateRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str
    content: str

    class Config: 
        from_attributes = True


class MessageResponse(BaseModel):
    id: str
    node_id: str
    sender: str
    content: str
    created_at: datetime

    class Config: 
        from_attributes = True