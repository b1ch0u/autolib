from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas
from .utils import get_random_printable_str


def get_user(session: Session, user_id: int):
    return session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(session: Session, email: str):
    return session.query(models.User).filter(models.User.email == email).first()


def create_user(
    session: Session,
    pwd_context:CryptContext,
    user: schemas.UserCreate
):
    salt = get_random_printable_str()
    hashed_password = pwd_context.hash(salt + user.password)
    db_user = models.User(
        email=user.email,
        salt=salt,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_free_cars(session: Session, seats: int | None = None):
    query = session.query(models.Car)
    if seats:
        query = query.filter(models.Car.model.seats >= seats)
    return query.all()
