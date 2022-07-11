from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Welcome to AutolibAPI. Have a look around (see swagger at /docs)'}


def test_create_user():
    response = client.post(
        '/users',
        json={'email': 'testemail', 'password': 'testpwd'}
    ).json()
    assert len(response) == 3
    assert 'id' in response
    assert response['email'] == 'testemail'
    assert response['car'] == None


def test_get_token():
    _ = client.post(
        '/users',
        json={'email': 'testemail', 'password': 'testpwd'}
    ).json()

    token = client.post(
        '/token',
        json={'email': 'testemail', 'password': 'testpwd'}
    ).json()
    assert len(response) == 2
    assert 'access_token' in token
    assert 'token_type' in token
