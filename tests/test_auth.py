def test_register_and_dashboard(client):
    r = client.post("/auth/register", data={"name": "Ann", "email": "a@x.com",
                    "password": "secret123", "confirm": "secret123"}, follow_redirects=True)
    assert r.status_code == 200 and b"Your learning paths" in r.data


def test_login_wrong_password(client, auth_client):
    client.post("/auth/logout")
    r = client.post("/auth/login", data={"email": "t@example.com", "password": "nope"})
    assert b"incorrect" in r.data


def test_dashboard_requires_login(client):
    r = client.get("/dashboard")
    assert r.status_code == 302 and "/auth/login" in r.headers["Location"]
