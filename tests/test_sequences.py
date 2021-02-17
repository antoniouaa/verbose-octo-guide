import json


def test_all_sequences_empty(app):
    response = app.get("/seq")

    expected_data = []
    expected_links = {"self": "http://localhost/seq"}
    expected_length = 0

    assert response.status_code == 200
    assert expected_data == response.json["data"]
    assert expected_links == response.json["links"]
    assert expected_length == response.json["meta"]["length"]


def test_all_sequencers_populated(app, make_root):
    root = json.dumps(make_root())
    assert isinstance(root, str)

    headers = {"Content-Type": "application/json"}

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    response = app.post("/user/login/", data=root, headers=headers)
    assert "data" in response.json

    token = str(response.json["data"]["token"])

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    human = {
        "description": "Human protein 1",
        "species": "Homo sapiens",
        "sequence": "ACGT",
        "type": "PROTEIN_FULL",
    }
    dog = {
        "description": "Canine RNA 1",
        "species": "Canis lupus",
        "sequence": "TGCA",
        "type": "RNA",
    }
    response = app.post("/seq", data=json.dumps(human), headers=headers)
    assert response.status_code == 201

    response = app.post("/seq", data=json.dumps(dog), headers=headers)
    assert response.status_code == 201

    response = app.get("/seq")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["meta"]["length"] == 2
    assert response.json["links"] == {"self": "http://localhost/seq"}
    assert response.json["data"][0]["attributes"]["species"] == human["species"]