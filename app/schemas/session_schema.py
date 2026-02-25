from pydantic import BaseModel
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int

class SessionResponse(BaseModel):
    id: int
    user_id: int
    started_at: datetime

    class Config:
        from_attributes = True