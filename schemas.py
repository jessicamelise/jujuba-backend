from pydantic import BaseModel, Field

class BaseUser(BaseModel):
    name: str = Field(..., max_length=100)
    role: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    active: bool = Field(False)

    class Config:
        orm_mode: True

class User(BaseUser):
    id: int

class CreateUser(BaseUser):
    password: str = Field(..., max_length=100)

class BaseProduct(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=200)
    price: str = Field(..., max_length=20)
    type: str = Field(..., max_length=50)

    class Config:
        orm_mode: True

class Product(BaseProduct):
    id: int