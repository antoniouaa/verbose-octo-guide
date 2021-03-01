from sequencer import create_app
from sequencer.config import DevelopmentConfig, ProductionConfig


def test_production_config():
    app = create_app(ProductionConfig)
    assert "production" == app.config["ENV"]
    assert not app.config["DEBUG"]


def test_development_config():
    app = create_app(DevelopmentConfig)
    assert "development" == app.config["ENV"]
    assert app.config["DEBUG"]


def test_root_user(make_root):
    root = make_root()
    assert root["email"] is not None
    assert root["username"] is not None
    assert root["password"] is not None
