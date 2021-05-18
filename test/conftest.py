import os
import sys
import tempfile
import pytest

#dir_test = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, dir_test + "/../..")

from access_control import create_app
from access_control.db import db_create_database, db_get

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")

@pytest.fixture
def app():

    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app_access_control = create_app({"TESTING": True, "DATABASE": db_path})
    # create the database and load test data
    with app_access_control.app_context():
        db_create_database()
        db_get().executescript(_data_sql)

    return app_access_control    

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
