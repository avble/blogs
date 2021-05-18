import pytest
from flask import g
from flask import session

# View
def test_view_login(client):
    response = client.get("/auth/login")
    assert "Username" in response.data.decode('utf-8')
    assert "Password" in response.data.decode('utf-8')

    response = client.post('/auth/login', data={'username':'admin', 'password':'admin'})
    assert "Redirecting..." in response.data.decode('utf-8')

def test_view_login_1(client):
    response = client.get("/auth/login")
    assert "Username" in response.data.decode('utf-8')
    assert "Password" in response.data.decode('utf-8')

    response = client.post('/auth/login', data={'username':'fake', 'password':'fake'})
    assert "Error" in response.data.decode('utf-8')


def test_view_logout_1(client):
    response = client.post('/auth/login', data={'username':'fake', 'password':'fake'})
    assert "Error" in response.data.decode('utf-8')

    response = client.get('/auth/logout')
    assert 'Redirect' in response.data.decode('utf-8')
    assert 302 == response.status_code