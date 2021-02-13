def test_all_sequences_empty(testapp):
    response = testapp.get("/seq")

    expected_data = []
    expected_links = {"self": "http://localhost/seq"}
    expected_length = 0

    assert response.status_int == 200
    assert expected_data == response.json["data"]
    assert expected_links == response.json["links"]
    assert expected_length == response.json["meta"]["length"]


def test_all_sequencers_populated(testapp, make_root):
    root = make_root()
    response = testapp.post_json("/user/login", root)
    token = str(response.json["data"]["token"])
    headers = {"Authorization": f"Bearer {token}"}
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
    testapp.post_json("/seq", human, headers=headers)
    testapp.post_json("/seq", dog, headers=headers)

    response = testapp.get("/seq")

    assert response.status_int == 200
    assert response.content_type == "application/json"
    assert response.json["meta"]["length"] == 2
    assert response.json["links"] == {"self": "http://localhost/seq"}
    assert response.json["data"][0]["attributes"]["species"] == human["species"]

    # assert expected_data == response.json["data"]
    # assert expected_links == response.json["links"]