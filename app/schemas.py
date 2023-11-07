from typing import List, Optional
from pydantic import BaseModel, validator,Field
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

    @validator("role")
    def role_is_valid(cls, v):
        valid_roles = ["user", "admin"] 
        if v not in valid_roles:
            raise ValueError("Invalid role")
        return v

class User(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class UserInDB(BaseModel):
    username: str
    email: str
    role: str
    hashed_password: str

class Geolocation(BaseModel):
    county: str
    location: str

class RedFlagCreate(BaseModel):
    incident_type: str
    description: str
    attachments: Optional[str] = None  
    additional_details: Optional[str] = None
    county: Optional[str] = None
    location: str
    date: datetime = Field(default_factory=datetime.now)

class RedFlag(RedFlagCreate):
    id: int

    class Config:
        orm_mode = True

class InterventionCreate(BaseModel):
    title: str
    description: str
    attachments: Optional[str] = None 
    additional_details: Optional[str] = None
    county: Optional[str] = None
    location: str
    date: datetime = Field(default_factory=datetime.now)

class Intervention(InterventionCreate):
    id: int

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    file_path: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True

class VideoBase(BaseModel):
    file_path: str

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    message: str
    is_email: bool
    is_sms: bool

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class AdminActionBase(BaseModel):
    user_id: int
    record_id: int
    action: str
    timestamp: str

class AdminActionCreate(AdminActionBase):
    pass

class AdminAction(AdminActionBase):
    id: int

    class Config:
        orm_mode = True

class Status(BaseModel):
    id: int
    name: str       

class StatusCreate(BaseModel):
    name: str

    @validator("name")
    def name_is_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Status name must be a string")
        return v

    class Config:
        orm_mode = True



