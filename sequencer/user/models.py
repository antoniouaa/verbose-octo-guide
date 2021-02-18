from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from sequencer.extensions import db


class User(db.Model):
    __tablename__ = "app_user"
    __name__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = User._hash_password(password)

    def _check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def _hash_password(password):
        return generate_password_hash(password)

    def __repr__(self):
        return f"<User: id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
        }


def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return user
