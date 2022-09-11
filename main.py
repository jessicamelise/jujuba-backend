from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    role: str
    email: str
    id: int

users: List[User] = []

def get_all_users() -> List[User]:
    return users

def get_user_by_id(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user
                 

def post_new_user(new_user: User) -> User:
    new_user.id = len(users) + 1
    users.append(new_user)
    return new_user


@app.get("/users")
def get_users():
    return get_all_users()


@app.get("/user/{user_id}")
def get_user(user_id: int):
    return get_user_by_id(user_id)


@app.post("/users")
def post_user(user: User):
    return post_new_user(user)