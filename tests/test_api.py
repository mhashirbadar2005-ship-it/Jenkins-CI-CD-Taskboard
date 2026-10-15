def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_index_serves_frontend(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Board" in response.text


def test_list_is_empty_at_start(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_list_task(client):
    created = client.post("/api/tasks", json={"title": "Write the Jenkinsfile"})
    assert created.status_code == 201
    body = created.json()
    assert body["title"] == "Write the Jenkinsfile"
    assert body["done"] is False

    listed = client.get("/api/tasks").json()
    assert [task["title"] for task in listed] == ["Write the Jenkinsfile"]


def test_create_rejects_blank_title(client):
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_mark_task_done(client):
    task_id = client.post("/api/tasks", json={"title": "Run tests"}).json()["id"]
    response = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True


def test_update_missing_task_returns_404(client):
    response = client.patch("/api/tasks/999", json={"done": True})
    assert response.status_code == 404


def test_delete_task(client):
    task_id = client.post("/api/tasks", json={"title": "Delete me"}).json()["id"]
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get("/api/tasks").json() == []
