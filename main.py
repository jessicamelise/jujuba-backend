from typing import List

from fastapi import FastAPI, HTTPException, status, Depends

from fastapi.middleware.cors import CORSMiddleware

from schemas import BaseUser, User, CreateUser

from sqlalchemy.orm import Session

from database import engine, get_db

import models

from dotenv import load_dotenv
load_dotenv()

models.Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users", response_model=List[User], status_code=200)
def get_users(db: Session = Depends(get_db)):
    db_users=db.query(models.User).all()
    return [User(**user.__dict__) for user in db_users]


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return User(**db_user.__dict__)


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    new_user = user.dict()
    db_new_user = models.User(**new_user)
    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)
    return User(**db_new_user.__dict__)


@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user: BaseUser, user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    db_update_user=db.query(models.User).filter(models.User.id==user_id).first()
    if db_update_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    db_update_user.name=user.name
    db_update_user.email=user.email
    db_update_user.role=user.role
    db_update_user.active=user.active
    db.commit()
    db.refresh(db_update_user)
    return User(**db_update_user.__dict__)


@app.delete("/users/{user_id}", response_model=str, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    db.delete(db_user)
    db.commit()
    return "ok"

@app.get("/login", response_model=bool, status_code=status.HTTP_200_OK)
def log_in(
    email_user: str,
    password: str,
    db: Session = Depends(get_db)  
):
    db_user = db.query(models.User).filter(
        models.User.email==email_user, 
        models.User.password==password).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")
    return True
