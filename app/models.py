from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from abc import ABC, abstractmethod
from schema import Schema, And, Use, Optional


class BaseModel(db.Model):
    """
    Base class for all models
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_check = And(int, lambda i: i > 0)

    @classmethod
    def string_check(cls, length):
        return And(str, lambda s: len(s) > 0 and len(s) <= length)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.now()
        db.session.commit()


class Entity(BaseModel):
    """
    Base class for entities
    """
    __abstract__ = True
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())


# Many-to-many relation between UserGroup and User
group_association = db.Table('group_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('user_group_id', db.Integer, db.ForeignKey('user_group.id'), primary_key=True)
)


class User(Entity):
    __tablename__ = 'user'
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    groups = db.relationship('UserGroup',
                             secondary=group_association,
                             backref=db.backref('group_association',
                                                lazy='dynamic',
                                                order_by=username
                             )
    )
    posts = db.relationship('LinkedinPost',
                            backref='user',
                            lazy=True,
                            cascade="delete, all")
    def __init__(self,
                 username,
                 password,
                 first_name,
                 last_name,
                 id=None,
                 created_at=datetime.today(),
                 updated_at=datetime.today()):
        if id:
            self.id = id
        self.username = username
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<User #{}: {}>'.format(self.id, self.username)

    def serialize(self):
        return {"id": self.id,
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "created_at": self.created_at,
                "updated_at": self.updated_at
                }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_group_names(self):
        """
        Get a list of names for all the groups that the user is in
        """
        query = (db.session.
                 query(UserGroup).
                 join(User.groups).
                 filter(User.id == self.id).
                 with_entities(UserGroup.group_name))
        return list(map(lambda x: x[0], query.all()))

    def __posts_query(self):
        return LinkedinPost.query.filter_by(user_id=self.id)

    def get_posts(self):
        return self.__posts_query().all()

    def get_latest_post(self):
        return (self.__posts_query().
                order_by(LinkedinPost.created_at.desc()).
                first())


class LinkedinPost(Entity):
    __tablename__ = 'linkedin_post'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(512))
    statistics = db.relationship('LinkedinPostStatistic',
                                 backref='linkedin_post',
                                 lazy=True,
                                 cascade="delete, all")

    def __init__(self,
                 user_id,
                 id=None,
                 content="",
                 created_at=datetime.today(),
                 updated_at=datetime.today()):
        if id:
            self.id = id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Linkedin Post #{} by {}>'.format(self.id, self.user_id)

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "content": self.content,
                "created_at": self.created_at,
                "updated_at": self.updated_at
                }
    def __statisitcs_query(self):
        return LinkedinPostStatistic.query.filter_by(linkedin_post_id=self.id)

    def get_statistics(self):
        return self.__statisitcs_query().all()

    def get_latest_statistic(self):
        return (self.__statisitcs_query().
                order_by(LinkedinPostStatistic.created_at.desc()).
                first())


class LinkedinPostStatistic(Entity):
    __tablename__ = 'linkedin_post_statistic'
    linkedin_post_id = db.Column(db.Integer,
                                 db.ForeignKey('linkedin_post.id'),
                                 index=True)
    num_views = db.Column(db.Integer)
    num_likes = db.Column(db.Integer)
    num_comments = db.Column(db.Integer)

    def __init__(self,
                 linkedin_post_id,
                 id=None,
                 num_views=0,
                 num_likes=0,
                 num_comments=0,
                 created_at=datetime.today(),
                 updated_at=datetime.today()):
        if id:
            self.id = id
        self.linkedin_post_id = linkedin_post_id
        self.num_views = num_views,
        self.num_likes = num_likes,
        self.num_comments = num_comments,
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Linkedin Post Statistic #{} by {}>'.format(self.id, self.linkedin_post_id)

    def serialize(self):
        return {"id": self.id,
                "linkedin_post_id": self.linkedin_post_id,
                "num_views": self.num_views,
                "num_likes": self.num_likes,
                "num_comments": self.num_comments,
                "created_at": self.created_at,
                "updated_at": self.updated_at
                }

    def get_post(self):
        return LinkedinPost.query.filter_by(id=self.linkedin_post_id).first()

    def get_user(self):
        query = (db.session.
                 query(User).
                 join(User.posts).
                 filter(LinkedinPost.id == self.linkedin_post_id))
        return query.first()


class UserGroup(BaseModel):
    __tablename__ = 'user_group'
    group_name = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, group_name, id=None):
        if id:
            self.id = id
        self.group_name = group_name

    def __repr__(self):
        return '<Group #{}: {}>'.format(self.id, self.group_name)

    def serialize(self):
        return {"id": self.id,
                "group_name": self.group_name
                }


class RevokedToken(BaseModel):
    """
    Model for saving revoked tokens. These are used for logging out
    """
    __tablename__ = 'revoked_token'
    jti = db.Column(db.String(120), index=True)

    def __init__(self, jti, id=None):
        if id:
            self.id = id
        self.jti = jti

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

    def __repr__(self):
        return '<Token #{} by {}>'.format(self.id, self.jti)
