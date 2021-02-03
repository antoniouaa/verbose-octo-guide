from app import db


class Genome(db.Model):
    __tablename__ = "genome"
    __name__ = "genome"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    species = db.Column(db.String())
    sequence = db.Column(db.String())

    def __init__(self, species, description, sequence):
        self.species = species
        self.description = description
        self.sequence = sequence

    def __repr__(self):
        return f"<id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "species": self.species,
            "sequence": self.sequence,
        }
