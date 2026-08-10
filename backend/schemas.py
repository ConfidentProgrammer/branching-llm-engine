from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DBStatusResponse(BaseModel):
    status: str
    message: str
    test_query_result: Optional[int] = None
    timestamp: datetime

class NodeCreateRequest(BaseModel):
    id: str = Field(..., description="Unique identifier for the node (e.g., UUID or slug)")
    title: str = Field(..., max_length=255)
    parent_id: Optional[str] = Field(None, description="Parent node ID if this is a branch")
    content: str = Field(..., description="The core text content to be embedded for vector search")

class NodeResponse(BaseModel):
    id: str
    title: str
    parent_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True