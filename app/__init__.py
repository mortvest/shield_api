from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models

@app.cli.command('resetdb')
def resetdb_command():
    """Drops and creates the database and tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(app.config['DB_URL']):
        print("Deleting database")
        drop_database(app.config['DB_URL'])
    if not database_exists(app.config['DB_URL']):
        print("Creating database")
        create_database(app.config['DB_URL'])

    print("Creating tables")
    db.create_all()
    print("Done")

@app.cli.command('add_toydata')
def add_toydata_command():
    """Adds toydata to tables for testing """

    print("Adding toy data")
    users = [models.User(1, "David", "Smith"),
             models.User(2, "John", "Doe"),
             models.User(3, "Mike", "Loke")
    ]
    for u in users:
        db.session.add(u)
    db.session.commit()
    print("Done")
