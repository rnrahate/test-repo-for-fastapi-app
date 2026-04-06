from .. import models,schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# this is a get request to fetch all the posts from the database 
# @router.get("/", response_model=list[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int=0,search: Optional[str]="",
            get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    print(limit,skip,search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #type: ignore

    post_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all() 
    return post_votes


# this is a post request to create a new post and add it to the database
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):  # type: ignore
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(get_current_user.user_id) # type:ignore
    post_dict = post.model_dump()
    new_post = models.Post(owner_id=get_current_user.user_id,**post_dict) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# this is a get request to fetch the latest post from the database
@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    # post = cursor.fetchone()
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return post


# this is a get request to fetch a specific post by its id from the database
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


# this is a delete request to delete a specific post by its id from the database
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                get_current_user: int = Depends(oauth2.get_current_user)):

    # deleting post logic
    # index = find_index_post(id)
    # if index is None:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    if post.owner_id != get_current_user.user_id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform request at action")
    
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# this is a put request to update a specific post by its id from the database
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                get_current_user: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()

    if post_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post_data.owner_id != get_current_user.user_id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform request at action")
    
    # Update the post fields
    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(post_data, key, value)

    db.commit()
    db.refresh(post_data)

    return post_data
