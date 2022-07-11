from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    salt = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    car = relationship('Car', back_populates='user', uselist=False)


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    model_id = Column(Integer, ForeignKey('car_models.id'), nullable=False)

    user = relationship('User', back_populates='car')
    model = relationship('CarModel', back_populates='cars', uselist=False)


class CarModel(Base):
    __tablename__ = 'car_models'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    seats = Column(Integer, index=True)

    cars = relationship('Car', back_populates='model')
