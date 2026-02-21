from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    lifetime_completions: int = 0
    is_cycle_completed: bool = False
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ReadingLogBase(BaseModel):
    start_page: int
    end_page: int

class ReadingLogCreate(ReadingLogBase):
    pass

class ReadingLogResponse(ReadingLogBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    target_pages: int
    target_days: int

class GoalCreate(GoalBase):
    pass

class GoalResponse(GoalBase):
    id: int
    user_id: int
    start_at: datetime
    status: str
    class Config:
        from_attributes = True
