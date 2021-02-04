from flask import Flask

import os
import dotenv

from . import views

dotenv.load_dotenv()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(views.genome_blueprint)

    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app


if __name__ == "__main__":
    app.run()
