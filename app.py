from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
import dotenv


dotenv.load_dotenv()

app = Flask(__name__)

app.config.from_object(os.getenv("APP_SETTINGS"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import Genome


@app.route("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
