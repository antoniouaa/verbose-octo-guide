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


def create_genome(species, description, sequence):
    genome = Genome(species=species, description=description, sequence=sequence)
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
