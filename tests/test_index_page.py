def test_index_page(testapp):
    response = testapp.get("/")

    expected_data = [{"Welcome to": "genome_sequencer!"}]
    expected_links = {"self": "http://localhost/"}

    assert response.status_int == 200
    assert response.content_type == "application/json"
    assert expected_data == response.json["data"]
    assert expected_links == response.json["links"]
