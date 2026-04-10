import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (nothing to set up for GET)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {test_email} for {activity}" in response.json().get("message", "")
    # Clean up: Remove test user if needed
    client.post(f"/activities/{activity}/unregister?email={test_email}")

def test_signup_duplicate():
    # Arrange
    test_email = "testuser2@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={test_email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={test_email}")

def test_unregister():
    # Arrange
    test_email = "testuser3@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={test_email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {test_email} from {activity}" in response.json().get("message", "")
