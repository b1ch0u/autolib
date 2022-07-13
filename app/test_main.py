import random as rd
from string import ascii_lowercase

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def create_random_user():
    mail = ''.join(rd.choice(ascii_lowercase) for _ in range(10)) + '@gmail.com'
    return client.post(
        '/users',
        json={
            'email': mail,
            'password': 'test-pwd'
        }
    ).json()


def create_random_user_and_get_token():
    user = create_random_user()
    email = user['email']
    return user, client.post(
        '/token',
        data={
            'username': email,
            'password': 'test-pwd'
        }
    ).json()


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Welcome to AutolibAPI. Have a look around (see swagger at /docs)'}


def test_create_user():
    user = create_random_user()
    assert len(user) == 3
    assert 'id' in user
    assert 'email' in user
    assert user['car'] == None
    return user


def test_get_token():
    _, token = create_random_user_and_get_token()
    assert len(token) == 2
    assert 'access_token' in token
    assert 'token_type' in token


def test_ask_car():
    user, token = create_random_user_and_get_token()
    car = client.post(
        '/users/me/car/rent',
        headers = {'Authorization': f'Bearer {token["access_token"]}'},
    ).json()
    assert 'x' in car
    assert 'y' in car
    print(car)
