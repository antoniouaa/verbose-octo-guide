import pytest
import os
import dotenv

dotenv.load_dotenv()

from sequencer import create_app
from sequencer.extensions import db as _db
from sequencer.config import TestingConfig


@pytest.fixture(scope="function")
def app():
    _app = create_app(TestingConfig)

    with _app.test_client() as testing_client:
        with _app.app_context():
            _db.create_all()
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
