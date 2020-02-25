import datetime as dt
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)

from app import routes, models

@app.cli.command('resetdb')
def resetdb_command():
    """Drops and creates the database and tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(app.config['DB_URL']):
        print("Dropping database")
        drop_database(app.config['DB_URL'])
    if not database_exists(app.config['DB_URL']):
        print("Creating database")
        create_database(app.config['DB_URL'])

    print("Creating tables")
    db.create_all()
    print("Done")

def add_objects(objects):
    for o in objects:
        db.session.add(o)

@app.cli.command('add_toydata')
def add_toydata_command():
    """Adds toydata to tables for testing """

    print("Adding toy data")
    now = dt.datetime.today()
    users = [models.User("dave11", "qwerty", "David", "Smith", now, now),
             models.User("john12", "qwerty", "John", "Doe", now, now),
             models.User("micko1", "qwerty", "Mike", "Loke", now, now)
    ]
    add_objects(users)
    db.session.commit()

    linkedin_posts = [models.LinkedinPost(1, 1, now, now),
                     models.LinkedinPost(2, 2, now, now)
    ]
    add_objects(linkedin_posts)
    db.session.commit()

    linkedin_post_stats = [models.LinkedinPostStatistic(1, 1, 0, 0, 0, now, now),
                          models.LinkedinPostStatistic(2, 2, 10, 0, 0, now, now)
    ]
    add_objects(linkedin_post_stats)
    db.session.commit()
    print("Done")
