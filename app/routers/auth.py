from fastapi import APIRouter ,Depends ,HTTPException ,status ,Response
from sqlalchemy.orm import Session
from ..database import *
from .. import schema ,models ,utils ,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Auth'])

@router.post('/login')
async def login(user_cred: OAuth2PasswordRequestForm = Depends() ,db: Session=Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                            detail="Invalid Credentials")
    
    if not utils.verify(user_cred.password ,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                            detail="Invalid Cred")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    token_type = "Bearer"

    return {"token": access_token ,"token_type": "bearer"}
