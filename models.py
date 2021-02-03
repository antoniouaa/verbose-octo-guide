from app import db


class Genome(db.Model):
    __tablename__ = "genome"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    sequence = db.Column(db.String())

    def __init__(self, name, author, sequence):
        self.name = name
        self.author = author
        self.sequence = sequence

    def __repr__(self):
        return f"<id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "sequence": self.sequence,
        }
