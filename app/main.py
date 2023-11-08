from fastapi import FastAPI ,Body ,Response ,status ,HTTPException ,Depends
from pydantic import BaseModel
from typing import Annotated,List
from random import randrange
import psycopg
from psycopg.rows import dict_row
from . import models
from .database import *
from sqlalchemy.orm import Session
from .schema import *
from . import utils
from .routers import user, post ,auth ,vote
from pydantic_settings import BaseSettings
from .config import *
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com" ,"https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#try:
#    conn = psycopg.connect(host="localhost" ,dbname='fastapi' ,user='postgres' ,
#                           password='1Deaajawen' ,row_factory=dict_row)
#    cur = conn.cursor()
#    print("Database connection was succesfull")
#except Exception as error:
#    print("Connecting to db failes")
#    print("Error: ",error)

my_posts = [
    {
        "title": "title of post 1" ,
        "content": "content of post 1",
        "id": 1
    } ,
    {
        "title": "favourite foods",
        "content": "I like pizza",
        "id": 2
    }
]

@app.get("/sqlalchemy")
async def test_orm(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "welcome to my api"}

