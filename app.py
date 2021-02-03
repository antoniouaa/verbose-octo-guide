from typing import Sequence
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException, NotFound

import os
import re
import dotenv


dotenv.load_dotenv()

app = Flask(__name__)

app.config.from_object(os.getenv("APP_SETTINGS"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import Genome


@app.route("/", methods=["GET"])
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


@app.route("/sequences", methods=["GET"])
def sample_genome():
    try:
        genomes = Genome.query.all()
        if not genomes:
            raise Exception("No genomes found in the Database")
        return (
            jsonify(
                {
                    "links": {
                        "self": request.url,
                    },
                    "data": [
                        {
                            "type": genome.__name__,
                            "id": genome.id,
                            "attributes": genome.serialize(),
                        }
                        for genome in genomes
                    ],
                }
            ),
            200,
        )
    except Exception as err:
        print(f"Error occured: {str(err)}")
        status = 404
        return (
            jsonify(
                {
                    "links": {
                        "self": request.url,
                    },
                    "errors": {
                        "method": request.method,
                        "status": str(status),
                        "details": str(err),
                    },
                }
            ),
            status,
        )


@app.route("/sequences", methods=["POST"])
def post_genome():
    description = request.form.get("description")
    species = request.form.get("species")
    sequence = request.form.get("sequence")
    if all((sequence, species, description)):
        try:
            genome = Genome(species=species, description=description, sequence=sequence)
            db.session.add(genome)
            db.session.commit()
            return (
                jsonify(
                    {
                        "links": {
                            "self": request.url,
                        },
                        "data": [
                            {
                                "type": genome.__name__,
                                "id": genome.id,
                                "attributes": genome.serialize(),
                            }
                        ],
                    }
                ),
                200,
            )
        except HTTPException as err:
            print(f"Error occured: {str(err)}")
            status = 400
            return (
                jsonify(
                    {
                        "links": {
                            "self": request.url,
                        },
                        "errors": {
                            "method": request.method,
                            "status": str(status),
                            "details": str(err),
                        },
                    }
                ),
                status,
            )


if __name__ == "__main__":
    app.run()
