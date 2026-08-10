from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DBStatusResponse(BaseModel):
    status: str
    message: str
    test_query_result: Optional[int] = None
    timestamp: datetime