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