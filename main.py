from typing import List

from fastapi import FastAPI, status

from schemas import BaseUser, User

from database import SessionLocal

import models

app = FastAPI()

db=SessionLocal()

@app.get("/users", response_model=List[User], status_code=200)
def get_users():
    db_users=db.query(models.User).all()
    return [User(**user.__dict__) for user in db_users]


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    db_user=db.query(models.User).filter(models.User.id==user_id).first()
    return User(**db_user.__dict__)


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: BaseUser):
    new_user = user.dict()
    db_user = models.User(**new_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)  


@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user: BaseUser, user_id: int):
    db_user=db.query(models.User).filter(models.User.id==user_id).first()
    db_user.name=user.name
    db_user.email=user.email
    db_user.role=user.role
    db_user.active=user.active
    db.commit()
    db.refresh(db_user)
    return User(**db_user.__dict__)


@app.delete("/user/{user_id}", response_model=str, status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    db_user=db.query(models.User).filter(models.User.id==user_id).first()
    db.delete(db_user)
    db.commit()
    return "ok"