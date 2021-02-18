import pytest
import os
import dotenv

dotenv.load_dotenv()

from sequencer import create_app
from sequencer.extensions import db as _db
from sequencer.config import TestingConfig
from sequencer.genome.models import Genome
from sequencer.user.models import User

human = {
    "description": "Human protein 1",
    "species": "Homo sapiens",
    "sequence": "ACGT",
    "type": "PROTEIN_FULL",
}

dog = {
    "description": "Canine RNA 1",
    "species": "Canis lupus",
    "sequence": "TGCA",
    "type": "RNA",
}

headers = {"Content-Type": "application/json"}


@pytest.fixture(scope="function")
def app(make_root):
    _app = create_app(TestingConfig)

    with _app.test_client() as testing_client:
        with _app.app_context():
            _db.drop_all()
            _db.create_all()
            root_credentials = make_root()
            test_root = User(**root_credentials)
            human_genome = Genome(**human)
            dog_genome = Genome(**dog)
            _db.session.add(test_root)
            _db.session.add(human_genome)
            _db.session.add(dog_genome)
            _db.session.commit()

            yield testing_client
            _db.session.close()
            _db.drop_all()


@pytest.fixture
def make_root():
    def get_root():
        return {
            "username": os.getenv("ROOT_USERNAME"),
            "password": os.getenv("ROOT_PASSWORD"),
        }

    return get_root
