from .. import models,schemas,utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hashed password
    hashed_password=utils.hash(user.password)
    user.password = hashed_password 
    
    # Create the user data dict
    user_dict = user.model_dump()
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/{user_id}',response_model=schemas.UserOut)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} does not exist")
    return user

