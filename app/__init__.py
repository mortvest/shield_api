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

    groups = [models.UserGroup("admin"),
              models.UserGroup("user")
              ]
    add_objects(groups)
    db.session.commit()

    users = [models.User("user1", "qwerty", "John", "Loke"),
             models.User("user2", "qwerty", "Michael", "Faraday")
    ]
    users[0].groups.append(groups[1])
    users[1].groups.append(groups[1])
    add_objects(users)

    au = models.User("admin", "qwerty", "John", "Doe")
    au.groups.append(groups[0])
    au.groups.append(groups[1])
    db.session.add(au)

    db.session.commit()

    linkedin_posts = [models.LinkedinPost(1, content="Content of Post 1"),
                      models.LinkedinPost(2, content="Content of Post 2")
    ]
    add_objects(linkedin_posts)
    db.session.commit()

    linkedin_post_stats = [models.LinkedinPostStatistic(1),
                          models.LinkedinPostStatistic(2)
    ]
    add_objects(linkedin_post_stats)
    db.session.commit()

    if users[0].get_posts():
        print("Status: working")
    else:
        print("Status: not working")

    print("Done")
