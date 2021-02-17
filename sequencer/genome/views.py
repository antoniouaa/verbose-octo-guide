from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
import time

blueprint = Blueprint("genome_blueprint", __name__)

from sequencer import utils
from sequencer.genome import models


@blueprint.route("/", methods=["GET"])
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


@blueprint.route("/", methods=["POST"])
@jwt_required
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
        201,
    )


@blueprint.route("/<id_>", methods=["GET"])
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


@blueprint.route("/<id_>", methods=["DELETE"])
@jwt_required
@utils.log_request
@utils.error_handler
def delete_genome_by_id(id_):
    models.delete_genome(id_)
    return ("", 204)


@blueprint.route("/<id_>", methods=["PATCH"])
@jwt_required
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
