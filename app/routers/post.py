from fastapi import FastAPI ,Response ,HTTPException ,Depends ,status ,APIRouter
from sqlalchemy.orm import Session
from .. import models ,schema ,utils ,oauth2
from ..database import get_db ,engine
from typing import List
from ..oauth2 import get_current_user
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/" ,response_model = List[schema.PostOut])
async def get_posts(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 2 ,skip: int=0 ,
                    search: str|None = ""):
    #cur.execute("""SELECT * FROM posts""")
    #posts = cur.fetchall()
    #print(posts)
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #res = db.query(models.Post ,func.count(models.Vote.post_id).label("votes")).join(models.Vote ,
    #                                 models.Vote.post_id == models.Post.id ,
    #                                 isouter=True).group_by(models.Post.id).all()
    res = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id ,isouter=True).group_by(
            models.Post.id).filter(
                models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(res)
    res = list(map(lambda x :x._mapping ,res))
    print(res)

    return res

#reading one post at a time with an id
@router.get("/{id}" ,response_model=schema.PostOut)
async def get_post(id: int ,db: Session = Depends(get_db)):
    
    #cur.execute("""SELECT * FROM posts WHERE id = %s """ ,(str(id),))
    #post = cur.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id ,isouter=True).group_by(
            models.Post.id).filter(id == models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Cant find post {404}"}
    
    print(post)
    print(post._mapping)

    post = post._mapping

    return post

@router.post("/" ,status_code=status.HTTP_201_CREATED ,response_model=schema.Post)
def create_posts(post: schema.BasePost, db: Session = Depends(get_db) ,
                 current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("INSERT INTO posts (title ,content ,published) VALUES (%s, %s, %s) RETURNING *", 
    #            (post.title, post.content, post.published))
    #new_post = cur.fetchone()
    #conn.commit()
    #return {"data": new_post}
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id ,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#Creating new data
#@app.post("/posts" ,status_code=status.HTTP_201_CREATED)
#async def create_posts(post: post_schema):
#    post_dict = post.model_dump()
#    post_dict["id"] = randrange(0 ,1000000)
#    my_posts.append(post_dict)
#    return {"data": post_dict}

@router.delete("/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int ,db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    #cur.execute("""DELETE FROM posts WHERE id = %s RETURNING * """ ,(str(id),))
    #deleted_post = cur.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                            detail="not authorized to perform requested action")
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="post with {id} doesnt exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}" ,response_model=schema.Post)
async def update_post(id:int ,post: schema.PostCreate ,
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #            (post.title ,post.content, post.published, str(id)))
    #new_post = cur.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                            detail="not authorized to perform requested action")
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="post with {id} doesnt exist")
    
    post_query.update(post.model_dump() ,synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}