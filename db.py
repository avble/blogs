import sqlite3
import click

from flask import current_app
from flask import g
from flask.cli import with_appcontext

def db_create_database():
    db = db_get()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def db_add_row_data():
    db = db_get()

    with current_app.open_resource("test_data.sql") as f:
        db.executescript(f.read().decode("utf8"))


def db_add_user(user, password):
    db = db_get()
    db.execute("INSERT INTO user (username, password) VALUES (\"%s\", \"%s\")" % (user, password))
    db.commit()

def db_get():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def db_close(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

@click.command("db-init", help="Initialize the database")
@with_appcontext
def db_create_database_cli():
    db_create_database()
    db_add_user("admin", "admin")


@click.command("db-init-data", help="Initialize the database with sample data")
@with_appcontext
def db_create_and_init_data_cli():
    db_create_database()
    db_add_user("admin", "admin")
    db_add_row_data()

@click.command("db-adduser", help="Add a username/password to database")
@click.option(
    "-u",
    "--username",
    "user",
    help="The username.",
)
@click.option(
    "-p",
    "--password",
    "password",
    help="The username.",
)
@with_appcontext
def db_add_user_cli(user, password):

    db_add_user(user, password)

def db_initialization(app):
    app.teardown_appcontext(db_close)
    app.cli.add_command(db_create_database_cli)
    app.cli.add_command(db_create_and_init_data_cli)
    app.cli.add_command(db_add_user_cli)