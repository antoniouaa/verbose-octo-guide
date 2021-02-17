import json
from tests.conftest import human, dog


def test_get_all_genomes(app):
    expected_links = {"self": "http://localhost/seq"}

    response = app.get("/seq")
    assert response.status_code == 200
    assert response.json["links"] == expected_links
    assert response.json["meta"]["length"] == 2


def test_post_genome(app, make_root):
    root = json.dumps(make_root())
    assert isinstance(root, str)

    headers = {"Content-Type": "application/json"}

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    response = app.post("/user/login/", data=root, headers=headers)
    assert "data" in response.json

    token = str(response.json["data"]["token"])

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    genome = {
        "description": "Cat protein 120",
        "species": "Felis catus",
        "sequence": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "type": "PROTEIN_FRAGMENT",
    }

    response = app.post("/seq", data=json.dumps(genome), headers=headers)
    assert response.status_code == 201
    assert response.content_type == "application/json"
    assert response.json["links"] == {"self": "http://localhost/seq"}
    assert response.json["data"][0]["attributes"]["species"] == genome["species"]
    assert response.json["data"][0]["attributes"]["sequence"] == genome["sequence"]
    assert response.json["data"][0]["attributes"]["type"] == genome["type"]
    assert (
        response.json["data"][0]["attributes"]["description"] == genome["description"]
    )


def test_get_genome_by_id(app):
    response = app.get("/seq/1")
    assert response.status_code == 200
    assert response.json["data"][0]["attributes"]["species"] == human["species"]
    assert response.json["data"][0]["attributes"]["sequence"] == human["sequence"]
    assert response.json["data"][0]["attributes"]["type"] == human["type"]
    assert response.json["data"][0]["attributes"]["description"] == human["description"]

    response = app.get("/seq/2")
    assert response.status_code == 200
    assert response.json["data"][0]["attributes"]["species"] == dog["species"]
    assert response.json["data"][0]["attributes"]["sequence"] == dog["sequence"]
    assert response.json["data"][0]["attributes"]["type"] == dog["type"]
    assert response.json["data"][0]["attributes"]["description"] == dog["description"]


def test_delete_genome_by_id(app, make_root):
    root = json.dumps(make_root())
    assert isinstance(root, str)

    headers = {"Content-Type": "application/json"}

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    response = app.post("/user/login/", data=root, headers=headers)
    assert "data" in response.json

    token = str(response.json["data"]["token"])

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = app.delete("/seq/1", headers=headers)
    assert response.status_code == 204
    assert response.json is None


def test_update_genome_by_id(app, make_root):
    root = json.dumps(make_root())
    assert isinstance(root, str)

    headers = {"Content-Type": "application/json"}

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    response = app.post("/user/login/", data=root, headers=headers)
    assert "data" in response.json

    token = str(response.json["data"]["token"])

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    patched_human = {
        "species": "Homo sapiens sapiens",
    }

    response = app.patch("/seq/1", data=json.dumps(patched_human), headers=headers)
    assert response.status_code == 200
    assert response.json["data"][0]["attributes"]["species"] == patched_human["species"]
