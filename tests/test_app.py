import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_activities_get():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_activity_signup():
    # Test signing up for an activity
    activity_name = "Chess Club"
    email = "test@example.com"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_activity_unregister():
    # First sign up a participant
    activity_name = "Chess Club"
    email = "test@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Then unregister them
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]