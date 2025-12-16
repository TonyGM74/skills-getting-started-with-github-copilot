import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_and_unregister():
    # Signup
    email = "testuser@mergington.edu"
    activity = "Soccer Team"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400  # 400 if already signed up
    # Unregister
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200 or unregister_resp.status_code == 404  # 404 if not found

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Basketball Club"
    # First signup
    client.delete(f"/activities/{activity}/unregister?email={email}")
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    # Duplicate signup
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_unregister_not_found():
    email = "notfound@mergington.edu"
    activity = "Art Club"
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404
