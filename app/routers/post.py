from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
# 444444444444444444444444444444444444444444444444444444444444444444444444 nebuvo from
from app import models, schemas, oauth2
# 555555555555555555555555555555555555555555555555555555555555555555555555 buvo from database import get_db
from app.database import get_db
from sqlalchemy import func

router =APIRouter(
    prefix="/posts",
    #swagger UI pagrupuot http://127.0.0.1:8001/docs
    tags={'Posts'}
)



#ORM example with Sqlalchemy ORM. No SQL code, just python code
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

#Importinam lists ir naudojam cia, kad visu postu listo nebandytu suskist i viena posta
@router.get("/", response_model=List[schemas.PostOut])
# def get_posts():
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #Joinai naudojami (left outer, siaip inner defaultas, todel prideda parametra isouter=True)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: Post):
#  #   print(post)
#     #converting to regular python dictionary
#  #   print(post.dict())
#     # post_dict = post.dict()
#     # post_dict['id'] = randrange(0, 100000)
#     # my_posts.append(post_dict)
#     #%s zemiau yra variables/placeholders in order to avoid sql injuections by using f'string method alternatively
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     #to return output from above
#     new_post = cursor.fetchone()
# #to actually commit data to database, otherwise it will not get written
#     conn.commit()

#depends oauth2 dependency forces users to be logged in to actually create a post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #lame way below, better is to unpack dictionary and convert into fomat below. In fenw fields wil be added (columns) in Post model, it will be automatically added
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
  
# title string, content string, nothing more

#{id} - path parameter, string, has to b econverted to integer
#PostOut - new format with the votes
@router.get("/{id}", response_model=schemas.PostOut)
#pirma eilute tieisog fastpi validationas, kad butu integeris, o ne asssafsfd, taip pat konveruoja i integeri
# def get_post(id: int):
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #first() unlike all() finds first result as it should in this case and ends querry
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
#    return{"post_detail": post}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
# db: Session = Depends(get_db) yra passing database dependency on the path operation function
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
#    if deleted_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: {id} does not exist")
    
    #delete only own posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
#session Basics -> Selecting a Synchronization Strategy prie SQLAlchemy 1.4 dokumentacijos galima rast naudojima, zemiau labiausiai patikima strategija
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
#post: Post to make sure that request comes with the right schema (defined above in class Post)
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
#    if updated_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: {id} does not exist")
    
    #checking if owner is actually owner of post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

 #   return {'data': updated_post}
    return post_query.first()