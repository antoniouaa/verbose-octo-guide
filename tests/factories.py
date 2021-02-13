from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory
import sqlalchemy

from sequencer.extensions import db
from sequencer.genome.models import Genome


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class GenomeFactory(BaseFactory):
    description = Sequence(lambda n: str(n).title())
    species = Sequence(lambda n: str(n).title())
    sequence = Sequence(lambda n: str(n).upper())
    type = Sequence(lambda n: str(n).upper())

    class Meta:
        model = Genome