from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.models.tree import Role
from app.schemas.member import MemberResponse

class TreeBase(BaseModel):
    generation_limit: int = 4

class TreeCreate(TreeBase):
    pass

class TreeResponse(TreeBase):
    id: int
    owner_id: int
    created_at: datetime
    members: List[MemberResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
