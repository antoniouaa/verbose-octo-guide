import pytest
import os
import dotenv

dotenv.load_dotenv()

from sequencer import create_app
from sequencer.config import TestingConfig
from sequencer.genome.models import Genome

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


@pytest.fixture(scope="function")
def app():
    _app, _db = create_app(TestingConfig)

    with _app.test_client() as testing_client:
        with _app.app_context():
            _db.create_all()
            human_genome = Genome(**human)
            dog_genome = Genome(**dog)
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
