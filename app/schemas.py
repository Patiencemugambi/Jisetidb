from typing import List, Optional
from pydantic import BaseModel, validator

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role: str = "user"

    @validator("role")
    def role_is_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Role must be a string")
        return v

class User(UserBase):
    id: int
    role: str
    login: "Login"

    class Config:
        orm_mode = True

class LoginBase(BaseModel):
    username: str
    user_id: int

class LoginCreate(LoginBase):
    password: str

class Login(LoginBase):
    id: int
    user: User

    class Config:
        orm_mode = True

class RedFlagBase(BaseModel):
    incident_type: str
    description: str
    attachments: Optional[str] = None  
    additional_details: Optional[str] = None
    county: Optional[str] = None
    location: str
    user_id: int
    status_id: int

class RedFlagCreate(RedFlagBase):
    pass

class RedFlag(RedFlagBase):
    id: int

    class Config:
        orm_mode = True

class InterventionBase(BaseModel):
    title: str
    description: str
    attachments: Optional[str] = None 
    additional_details: Optional[str] = None
    county: Optional[str] = None
    location: str
    user_id: int
    status_id: int

class InterventionCreate(InterventionBase):
    pass

class Intervention(InterventionBase):
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

class UserInDB(BaseModel):
    username: str
    hashed_password: str  

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
