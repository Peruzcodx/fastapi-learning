from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    name: str = Field(min_length=1)
    city: str = Field(min_length=1)

class UserCreate(BaseModel):
    name: str = Field(min_length = 1)
    city: str = Field(min_length = 1)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(BaseModel):
    name: str   |  None = Field (default=None, min_length=1)
    city: str   |None = Field (default=None, min_length=1) 

class LoginRequest(BaseModel):
    email: str 
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str