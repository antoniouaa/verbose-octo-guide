import json

from tests.conftest import headers


def test_get_all_users(app):
    expected_links = {"self": "http://localhost/user"}

    response = app.get("/user", headers=headers)
    assert response.status_code == 200
    assert response.json["links"] == expected_links
    assert response.json["data"] != []
    assert response.json["meta"]["length"] > 0


def test_signup(app):
    test_user = {"username": "test_username", "password": "test_password"}

    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 201
    assert response.json["data"]["attributes"]["username"] == test_user["username"]

    response = app.get("/user", headers=headers)
    assert response.status_code == 200

    usernames = [u["attributes"]["username"] for u in response.json["data"]]
    assert test_user["username"] in usernames


def test_login(app):
    test_user = {"username": "test_username", "password": "test_password"}

    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 201
    assert response.json["data"]["attributes"]["username"] == test_user["username"]

    response = app.post("/user/login", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 201
    assert response.json["data"]["token"] is not None
    assert response.json["data"]["attributes"]["username"] == test_user["username"]

    response = app.get("/user", headers=headers)
    assert response.status_code == 200
    assert response.json["meta"]["length"] == 2

    usernames = [u["attributes"]["username"] for u in response.json["data"]]
    assert test_user["username"] in usernames


def test_protected_resource(app):
    test_user = {"username": "test_username", "password": "test_password"}
    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    response = app.post("/user/login", data=json.dumps(test_user), headers=headers)

    token = str(response.json["data"]["token"])
    auth_headers = {**headers, "Authorization": f"Bearer {token}"}

    response = app.get("/user/protected", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["data"][0] == {
        "Protected": "resource!",
        "Logged in as": test_user["username"],
    }


def test_signup_badrequest(app):
    test_user = {"username": "test_username"}

    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 400
    assert response.json["errors"]["method"] == "POST"
    assert response.json["errors"]["details"] == "400 Bad Request: Password missing"

    test_user = {"password": "test_password"}

    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 400
    assert response.json["errors"]["method"] == "POST"
    assert response.json["errors"]["details"] == "400 Bad Request: Username missing"


def test_login_badrequest(app):
    test_user = {"username": "test_username", "password": "test_password"}
    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)

    test_user = {"username": "test_username"}

    response = app.post("/user/login", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 400
    assert response.json["errors"]["method"] == "POST"
    assert response.json["errors"]["details"] == "400 Bad Request: Password missing"

    test_user = {"password": "test_password"}

    response = app.post("/user/login", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 400
    assert response.json["errors"]["method"] == "POST"
    assert response.json["errors"]["details"] == "400 Bad Request: Username missing"


def test_signup_conflict(app):
    test_user = {"username": "test_username", "password": "test_password"}

    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 201

    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 409
    assert response.json["errors"]["method"] == "POST"
    assert response.json["errors"]["details"] == "409 Conflict: User already exists!"


def test_login_notfound(app):
    test_user = {"username": "test_username", "password": "test_password"}

    response = app.post("/user/login", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 404
    assert response.json["errors"]["method"] == "POST"
    assert response.json["errors"]["details"] == "404 Not Found: User does not exist"


def test_login_unauthorized(app, make_root):
    username, _ = make_root().values()
    test_user = {"username": username, "password": "test_password"}

    response = app.post("/user/login", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 401
    assert response.json["errors"]["method"] == "POST"
    assert (
        response.json["errors"]["details"] == "401 Unauthorized: Passwords don't match"
    )


def test_delete_user(app):
    test_user = {"username": "test_username", "password": "test_password"}

    response = app.post("/user/signup", data=json.dumps(test_user), headers=headers)
    assert response.status_code == 201

    response = app.post("/user/login", data=json.dumps(test_user), headers=headers)
    token = str(response.json["data"]["token"])
    auth_headers = {**headers, "Authorization": f"Bearer {token}"}

    response = app.delete("/user/delete", headers=auth_headers)
    assert response.status_code == 204
    assert response.json is None
