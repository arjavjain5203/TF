from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from app.models.member import Gender

class MemberBase(BaseModel):
    name: str
    dob: date
    gender: Gender
    phone: Optional[str] = None
    generation_level: int
    is_locked: bool = False
    locked_by: Optional[int] = None
    lock_expires_at: Optional[datetime] = None

class MemberCreate(MemberBase):
    tree_id: int

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None
    is_locked: Optional[bool] = None
    locked_by: Optional[int] = None
    lock_expires_at: Optional[datetime] = None

class MemberResponse(MemberBase):
    id: int
    tree_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
