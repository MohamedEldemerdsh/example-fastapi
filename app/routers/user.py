from fastapi import FastAPI ,Response ,HTTPException ,Depends ,status ,APIRouter
from sqlalchemy.orm import Session
from .. import models ,schema ,utils
from ..database import get_db ,engine
from typing import List
from ..schema import *

router = APIRouter(
    tags=['Users']
)

@router.post("/users" ,status_code=status.HTTP_201_CREATED ,response_model=UserOut)
async def create_user(user:CreateUser ,db: Session=Depends(get_db)):
    #hash password
    hashed_password = utils.hash(user.password)
    user.password=hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users/{id}' ,response_model=UserOut)
async def get_user(id: int ,db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f'user with {id} doesnt exist')
    return user