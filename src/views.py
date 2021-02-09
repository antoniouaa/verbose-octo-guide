from flask import jsonify, request, Blueprint
from werkzeug.exceptions import HTTPException
import time

import utils

genome_blueprint = Blueprint("genome_blueprint", __name__)

import models


@genome_blueprint.route("/", methods=["GET"])
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


@genome_blueprint.route("/sequences", methods=["GET"])
@utils.log_request
@utils.error_handler
def get_all_genomes():
    genomes = models.Genome.query.all()
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
                    if genome is not None
                ],
                "meta": {
                    "length": len(genomes),
                    "timestamp": int(time.time()),
                },
            }
        ),
        200,
    )


@genome_blueprint.route("/sequences", methods=["POST"])
@utils.log_request
@utils.error_handler
def post_genome():
    resp_data = request.get_json()
    description = resp_data.get("description")
    species = resp_data.get("species")
    sequence = resp_data.get("sequence")
    type_ = resp_data.get("type")
    genome = models.create_genome(species, description, sequence, type_)
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
                "meta": {
                    "timestamp": int(time.time()),
                },
            }
        ),
        200,
    )


@genome_blueprint.route("/sequences/<id_>", methods=["GET"])
@utils.log_request
@utils.error_handler
def get_genome_by_id(id_):
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
                "meta": {
                    "timestamp": int(time.time()),
                },
            }
        ),
        200,
    )


@genome_blueprint.route("/sequences/<id_>", methods=["DELETE"])
@utils.log_request
@utils.error_handler
def delete_genome_by_id(id_):
    models.delete_genome(id_)
    return ("", 204)


@genome_blueprint.route("/sequences/<id_>", methods=["PATCH"])
@utils.log_request
@utils.error_handler
def update_genome_by_id(id_):
    genome = models.update_genome(id_=id_, new_attrs=request.form)
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
                "meta": {
                    "timestamp": int(time.time()),
                },
            }
        ),
        200,
    )
