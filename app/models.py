from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self,
                 id,
                 first_name,
                 last_name,
                 created_at=datetime.today(),
                 updated_at=datetime.today()):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<User #{}: {} {}>'.format(self.id, self.first_name, self.last_name)

    def serialize(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "created_at": self.created_at,
                "updated_at": self.updated_at
                }


class LinkedinPost(db.Model):
    __tablename__ = 'linkedin_post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, id, user_id, created_at=datetime.today(), updated_at=datetime.today()):
        self.id = id
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Linkedin Post #{} by {}>'.format(self.id, self.user_id)

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "created_at": self.created_at,
                "updated_at": self.updated_at
                }


class LinkedinPostStatistic(db.Model):
    __tablename__ = 'linkedin_post_statistic'
    id = db.Column(db.Integer, primary_key=True)
    linkedin_post_id = db.Column(db.Integer, db.ForeignKey('linkedin_post.id'), index=True)
    num_views = db.Column(db.Integer)
    num_likes = db.Column(db.Integer)
    num_comments = db.Column(db.Integer)
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self,
                 id,
                 linkedin_post_id,
                 num_views=0,
                 num_likes=0,
                 num_comments=0,
                 created_at=datetime.today(),
                 updated_at=datetime.today()):
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
