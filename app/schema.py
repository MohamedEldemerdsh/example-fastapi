from pydantic import BaseModel ,EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_model=True

class BasePost(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(BasePost):
    pass

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_model = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_model = True