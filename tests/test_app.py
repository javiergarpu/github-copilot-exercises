import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Gym Class" in data
    assert "Programming Class" in data

def test_signup_success():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.get("/activities")
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400 or response.status_code == 200
    if response.status_code == 400:
        assert response.json()["detail"] == "Student already signed up for this activity"
    else:
        assert response.json()["message"].startswith("Signed up")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
