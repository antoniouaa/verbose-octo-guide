import json


def test_get_all_genomes(app):
    response = app.get("/seq")

    expected_data = []
    expected_links = {"self": "http://localhost/seq"}
    expected_length = 0

    assert response.status_code == 200
    assert expected_data == response.json["data"]
    assert expected_links == response.json["links"]
    assert expected_length == response.json["meta"]["length"]


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
    assert response.json["data"][-1]["attributes"]["species"] == genome["species"]


def test_get_genome_by_id(app):
    response = app.get("/seq")
