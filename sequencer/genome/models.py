from datetime import datetime

from dna_toolkit import toolkit

from sequencer.extensions import db


class Genome(db.Model):
    __tablename__ = "genome"
    __name__ = "genome"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    species = db.Column(db.String(), nullable=False)
    sequence = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    gc_content = db.Column(db.Integer, nullable=True)
    rna_transcription = db.Column(db.String(), nullable=True)
    reverse_complement = db.Column(db.String(), nullable=True)

    def __init__(self, species, description, sequence, type):
        self.species = species
        self.description = description
        self.sequence = sequence
        self.type = type
        self.gc_content = toolkit.gc_content(self.sequence)
        self.rna_transcription = toolkit.transcription(self.sequence)
        self.reverse_complement = toolkit.reverse_comp(self.sequence)

    def __repr__(self):
        return f"<Genome: id {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "species": self.species,
            "sequence": self.sequence,
            "type": self.type,
            "dna_attributes": {
                "gc_content": self.gc_content,
                "rna_transcription": self.rna_transcription,
                "reverse_complement": self.reverse_complement,
            },
        }


def create_genome(species, description, sequence, type):
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
        setattr(genome, attr, new_value.strip())
    genome.updated_on = datetime.utcnow()
    db.session.commit()
    return genome
