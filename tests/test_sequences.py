import json
from tests.conftest import human, dog, giraffe, headers


def test_get_all_genomes(app):
    expected_links = {"self": "http://localhost/seq"}

    response = app.get("/seq", headers=headers)
    assert response.status_code == 200
    assert response.json["links"] == expected_links
    assert response.json["meta"]["length"] == 2


def test_post_genome(app, make_root):
    root = json.dumps(make_root())
    assert isinstance(root, str)

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    response = app.post("/user/login/", data=root, headers=headers)
    assert "data" in response.json

    token = str(response.json["data"]["token"])

    auth_headers = {**headers, "Authorization": f"Bearer {token}"}
    test_genome = giraffe

    response = app.post("/seq", data=json.dumps(test_genome), headers=auth_headers)
    assert response.status_code == 201
    assert response.content_type == "application/json"
    assert response.json["links"] == {"self": "http://localhost/seq"}
    assert response.json["data"]["attributes"]["species"] == test_genome["species"]
    assert response.json["data"]["attributes"]["sequence"] == test_genome["sequence"]
    assert response.json["data"]["attributes"]["type"] == test_genome["type"]
    assert (
        response.json["data"]["attributes"]["description"] == test_genome["description"]
    )


def test_get_genome_by_id(app):
    response = app.get("/seq/1", headers=headers)
    assert response.status_code == 200
    assert response.json["data"]["attributes"]["species"] == human["species"]
    assert response.json["data"]["attributes"]["sequence"] == human["sequence"]
    assert response.json["data"]["attributes"]["type"] == human["type"]
    assert response.json["data"]["attributes"]["description"] == human["description"]

    response = app.get("/seq/2", headers=headers)
    assert response.status_code == 200
    assert response.json["data"]["attributes"]["species"] == dog["species"]
    assert response.json["data"]["attributes"]["sequence"] == dog["sequence"]
    assert response.json["data"]["attributes"]["type"] == dog["type"]
    assert response.json["data"]["attributes"]["description"] == dog["description"]


def test_delete_genome_by_id(app, make_root):
    root = json.dumps(make_root())
    assert isinstance(root, str)

    headers = {"Content-Type": "application/json"}

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    response = app.post("/user/login/", data=root, headers=headers)
    token = str(response.json["data"]["token"])
    auth_headers = {**headers, "Authorization": f"Bearer {token}"}

    response = app.delete("/seq/1", headers=auth_headers)
    assert response.status_code == 204
    assert response.json is None


def test_update_genome_by_id(app, make_root):
    root = json.dumps(make_root())
    assert isinstance(root, str)

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    response = app.post("/user/login/", data=root, headers=headers)
    assert "data" in response.json

    token = str(response.json["data"]["token"])
    auth_headers = {**headers, "Authorization": f"Bearer {token}"}

    patched_human = {
        "species": "Homo sapiens sapiens",
    }

    response = app.patch("/seq/1", data=json.dumps(patched_human), headers=auth_headers)
    assert response.status_code == 200
    assert response.json["data"]["attributes"]["species"] == patched_human["species"]
