from app.api.security import Hasher
from app.database.models.user import User
from fastapi import HTTPException, status
from .schemas import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound


def create_new_user(user: UserCreate, db: Session):
    try:
        user = User(
            name=user.name,
            email=user.email,
            hashed_password=Hasher.get_password_hash(user.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exist')


def get_user_by_email(email: str, db: Session):
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user found')

