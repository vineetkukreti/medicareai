from pydantic import BaseModel, EmailStr
from datetime import datetime

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class Contact(ContactCreate):
    id: int
    class Config:
        from_attributes = True

class ContactResponse(ContactCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class AdminReplyRequest(BaseModel):
    message: str
