from flask import Flask, jsonify, request

from sequencer.extensions import db, jwt, cors, migrate
from sequencer.config import ProductionConfig
from sequencer.genome.models import Genome
from sequencer import utils, genome, user

# from sequencer.user.models import User


def create_app(config=ProductionConfig):
    app = Flask(__name__.split(".")[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    register_blueprint(app)

    @app.route("/", methods=["GET"])
    @utils.log_request
    @utils.error_handler
    def index():
        return (
            jsonify(
                {
                    "links": {
                        "self": request.url,
                    },
                    "data": [{"Welcome to": "genome_sequencer!"}],
                }
            ),
            200,
        )

    return app, db


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)


def register_blueprint(app):
    origins = app.config.get("CORS_ORIGIN_WHITELIST", "*")
    cors.init_app(user.views.blueprint, origins=origins)
    cors.init_app(genome.views.blueprint, origins=origins)

    app.register_blueprint(user.views.blueprint, url_prefix="/user")
    app.register_blueprint(genome.views.blueprint, url_prefix="/seq")
