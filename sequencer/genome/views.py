from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import Unauthorized
import time
import os

blueprint = Blueprint("genome_blueprint", __name__)

from sequencer import utils
from sequencer.genome import models


@blueprint.route("/", methods=["GET"])
@utils.log_request
@utils.error_handler
def get_all_genomes():
    genomes = models.Genome.query.all()
    return (
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
        },
        200,
    )


@blueprint.route("/", methods=["POST"])
@utils.log_request
@utils.error_handler
@jwt_required
def post_genome():
    resp_data = request.get_json()
    description = resp_data.get("description")
    species = resp_data.get("species")
    sequence = resp_data.get("sequence")
    type_ = resp_data.get("type")
    genome = models.create_genome(species, description, sequence, type_)
    return (
        {
            "links": {
                "self": request.url,
            },
            "data": {
                "type": genome.__name__,
                "id": genome.id,
                "attributes": genome.serialize(),
            },
            "meta": {
                "timestamp": int(time.time()),
            },
        },
        201,
    )


@blueprint.route("/<id_>", methods=["GET"])
@utils.log_request
@utils.error_handler
def get_genome_by_id(id_):
    genome = models.Genome.query.filter_by(id=id_).first_or_404()
    return (
        {
            "links": {
                "self": request.url,
            },
            "data": {
                "type": genome.__name__,
                "id": genome.id,
                "attributes": genome.serialize(),
            },
            "meta": {
                "timestamp": int(time.time()),
            },
        },
        200,
    )


@blueprint.route("/<id_>", methods=["DELETE"])
@utils.log_request
@utils.error_handler
@jwt_required
def delete_genome_by_id(id_):
    current_user = get_jwt_identity()
    if current_user["username"] != os.getenv("ROOT_USERNAME"):
        raise Unauthorized("You don't have enough permissions for that action.")
    models.delete_genome(id_)
    return ("", 204)


@blueprint.route("/<id_>", methods=["PATCH"])
@utils.log_request
@utils.error_handler
@jwt_required
def update_genome_by_id(id_):
    current_user = get_jwt_identity()
    if current_user["username"] != os.getenv("ROOT_USERNAME"):
        raise Unauthorized("You don't have enough permissions for that action.")
    genome = models.update_genome(id_=id_, new_attrs=request.json)
    return (
        {
            "links": {
                "self": request.url,
            },
            "data": {
                "type": genome.__name__,
                "id": genome.id,
                "attributes": genome.serialize(),
            },
            "meta": {
                "timestamp": int(time.time()),
            },
        },
        200,
    )
