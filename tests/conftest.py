import pytest
import os
import dotenv
from webtest import TestApp

dotenv.load_dotenv()

from sequencer import create_app
from sequencer.extensions import db as _db
from sequencer.config import TestingConfig
from sequencer.genome.models import Genome
from .factories import GenomeFactory


@pytest.fixture(scope="function")
def app():
    _app = create_app(TestingConfig)

    with _app.test_request_context():
        yield _app


@pytest.fixture(scope="function")
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


# @pytest.fixture(scope="function")
# def db(app):
#     _db.app = app
#     with app.app_context():
#         _db.create_all()

#     yield _db
#     _db.session.close()
#     _db.drop_all()


@pytest.fixture
def make_root():
    def get_root():
        return {
            "username": os.getenv("ROOT_USERNAME"),
            "password": os.getenv("ROOT_PASSWORD"),
        }

    return get_root