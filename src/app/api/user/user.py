from .crud import create_new_user
from app.database.db import get_db
from fastapi import APIRouter, Depends
from .schemas import ShowUser, UserCreate
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['user'],
    prefix='/v1/user',
    responses={404: {'description': 'Not found'}},
)


@router.post("/signup", response_model=ShowUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
