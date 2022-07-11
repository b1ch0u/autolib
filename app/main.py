from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import crud, models, schemas
from .database import get_db, engine
from .authentication import *


ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post('/users', response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    session: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail='Email already registered'
        )
    return crud.create_user(session=session, pwd_context=pwd_context, user=user)


@app.post('/token', response_model=schemas.Token)
def login_for_access_token(
    session: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users/me/', response_model=schemas.User)
def read_users_me(user: schemas.User = Depends(get_current_user)):
    return user


@app.get('/users/me/car/', response_model=schemas.Car)
def read_users_car(user: schemas.User = Depends(get_current_user)):
    return user.car


@app.post('/users/me/car/rent', response_model=schemas.Car)
def ask_for_a_car(
    session: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
    seats: int | None = None
):
    if user.car:
        return user.car

    try:
        car: models.Car = next(iter(crud.get_free_cars(session, seats)))
    except StopIteration:
        return {'error': 'No car available at the moment'}

    car.user_id = user.id
    session.commit()
    return car


@app.post('/users/me/car/return', response_model=schemas.Car)
def return_car(
    new_x: int,
    new_y: int,
    session: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    if not user.car:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No car currently associated to this user'
            headers={'WWW-Authenticate': 'Bearer'},
        )

    car = user.car
    car.user_id = None
    car.x = new_x
    car.y = new_y
    session.commit()
    return {}


@app.get('/')
def greet_home():
    return {'msg': 'Welcome to AutolibAPI. Have a look around (see swagger at /docs)'}
