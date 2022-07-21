from pydantic import BaseModel
from pydantic import EmailStr


# properties required during user creation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    name: str
    email: EmailStr

    class Config:  # to convert non dict obj to json
        orm_mode = True
