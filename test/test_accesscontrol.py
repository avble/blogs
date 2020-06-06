import pytest
from flask import g
from flask import session


# View
def test_view_index(client, auth):
    response = client.get("/")

    assert "Redirecting..." in response.data.decode('utf-8')

    auth.login('admin', 'admin')
    response = client.get("/")
    assert "access-control" in response.data.decode('utf-8')
    assert "Code" in response.data.decode('utf-8')
    assert "ShareInfo" in response.data.decode('utf-8')

    #print(response.data.decode('utf-8'))


def test_view_delete(client):
    response = client.post('/accesscontrol/delete/123465')
    data = response.data.decode('utf-8')
    assert response.status_code == 302 # Status code
    assert 'redirect' in data

    response = client.get('/accesscontrol/get/123465')
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    print ('--------------------------------')
    print (data)
    print ('--------------------------------')
    assert data == 'NONE'


# RestAPI
def test_api_get_1(client):
    response = client.get("/accesscontrol/get/123456")
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    
def test_api_register_1(client):
    response = client.post("/accesscontrol/register")
    assert response.status_code == 200
    code = response.data.decode('utf-8')
    assert len(code) == 6

    response = client.get("/accesscontrol/get/%s" % (code))
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    