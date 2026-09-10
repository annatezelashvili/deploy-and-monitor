from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_add_tasks():
    task = {"title": "study"}
    response =  client.post("/tasks", json=task)
    assert response.status_code == 200
    assert response.json()["title"] == task["title"]

def test_delete_task():
    task = {"title": "work out"}
    create_response = client.post("/tasks", json=task)
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

def test_task_delete_nonexistent_task():
    response = client.delete("/tasks/999")
    assert response.status_code == 404

def test_get_tasks():
    task = {"title": "doctor appointment"}
    create_response = client.post("/tasks",json=task)
    task_id=create_response.json()["id"]

    get_response = client.get("/tasks")
    assert get_response.status_code == 200
    assert isinstance(get_response.json(),list) 
    
    matching_tasks = [t for t in get_response.json() if t["id"] == task_id]
    assert len(matching_tasks) == 1
    assert matching_tasks[0]["title"] == task["title"]
    