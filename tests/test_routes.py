def _generate(client):
    return client.post("/generate", data={"goal": "web developer", "level": "beginner",
                       "hours_per_week": 5, "total_weeks": 6, "interests": "python"})


def test_generate_and_view(auth_client):
    r = _generate(auth_client)
    assert r.status_code == 302
    page = auth_client.get(r.headers["Location"])
    assert page.status_code == 200 and b"Week 1" in page.data


def test_toggle_progress(auth_client):
    _generate(auth_client)
    r = auth_client.post("/path/1/toggle/1")
    assert r.get_json()["done"] is True


def test_delete(auth_client):
    _generate(auth_client)
    auth_client.post("/path/1/delete")
    assert auth_client.get("/path/1").status_code == 404


def test_404_page(client):
    assert client.get("/nope").status_code == 404
