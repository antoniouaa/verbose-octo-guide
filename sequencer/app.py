from flask import Flask


from sequencer.extensions import db, jwt, cors, migrate
from sequencer.config import ProductionConfig
from sequencer import views


def create_app(config=ProductionConfig):
    app = Flask(__name__.split(".")[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    register_blueprint(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)


def register_blueprint(app):
    origins = app.config.get("CORS_ORIGIN_WHITELIST", "*")
    cors.init_app(views.blueprint, origins=origins)

    app.register_blueprint(views.blueprint)
