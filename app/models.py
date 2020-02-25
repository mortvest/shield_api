from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    # created_at = db.Column(db.Date())
    # updated_at = db.Column(db.Date())

    # def __init__(self, id, first_name, last_name, created_at, updated_at):
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)

    def serialize(self):
        return {"id": self.id, "first_name": self.first_name, "last_name":self.last_name}

# class LinkedinPost(db.Model):
