from flask import jsonify, request, Blueprint
from werkzeug.exceptions import HTTPException

import utils

genome_blueprint = Blueprint("genome_blueprint", __name__)

import models


@genome_blueprint.route("/", methods=["GET"])
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


@genome_blueprint.route("/sequences", methods=["GET"])
@utils.log_request
def get_all_genomes():
    try:
        genomes = models.Genome.query.all()
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
    except HTTPException as err:
        status = err.get_response().status
        return jsonify(utils.handle_error(request=request, err=err, status=status))
    except Exception as err:
        status = err.get_response().status
        return jsonify(utils.handle_error(request=request, err=err, status=status))


@genome_blueprint.route("/sequences", methods=["POST"])
@utils.log_request
def post_genome():
    description = request.form.get("description")
    species = request.form.get("species")
    sequence = request.form.get("sequence")
    if all((sequence, species, description)):
        try:
            genome = models.create_genome(species, description, sequence)
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
            status = err.get_response().status
            return jsonify(utils.handle_error(request=request, err=err, status=status))


@genome_blueprint.route("/sequences/<id_>", methods=["GET"])
@utils.log_request
def get_genome_by_id(id_):
    try:
        genome = models.Genome.query.filter_by(id=id_).first_or_404()
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
        status = err.get_response().status
        return (
            jsonify(utils.handle_error(request=request, err=err, status=status)),
            status,
        )