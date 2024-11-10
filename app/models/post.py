from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    author_id: str
    tags: List[str] = []
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    likes: int = 0
