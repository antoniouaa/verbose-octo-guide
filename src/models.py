from app import db


class Genome(db.Model):
    __tablename__ = "genome"
    __name__ = "genome"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    species = db.Column(db.String(), nullable=False)
    sequence = db.Column(db.String(), nullable=False, unique=True)
    type = db.Column(db.String(), nullable=False)

    def __init__(self, species, description, sequence, type):
        self.species = species
        self.description = description
        self.sequence = sequence
        self.type = type

    def __repr__(self):
        return f"<id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "species": self.species,
            "sequence": self.sequence,
            "type": self.type,
        }


def create_genome(species, description, sequence, type=None):
    genome = Genome(
        species=species, description=description, sequence=sequence, type=type
    )
    db.session.add(genome)
    db.session.commit()
    return genome


def delete_genome(id_):
    genome = Genome.query.filter_by(id=id_).first_or_404()
    db.session.delete(genome)
    db.session.commit()
    return genome


def update_genome(id_, new_attrs):
    genome = Genome.query.filter_by(id=id_).first_or_404()
    for attr, new_value in new_attrs.items():
        setattr(genome, attr, new_value)
    db.session.commit()
    return genome
