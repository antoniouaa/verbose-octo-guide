from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from sequencer.extensions import db


class User(db.Model):
    __tablename__ = "app_user"
    __name__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password_hash = self._hash_password(str(password))

    def _hash_password(self, password):
        return generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User: id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
        }


def create_user(username, password, email):
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return user
