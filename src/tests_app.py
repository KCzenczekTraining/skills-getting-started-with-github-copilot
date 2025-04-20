# Test cases for the FastAPI application

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert str(response.url).endswith("/static/index.html")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up newstudent@mergington.edu for Chess Club"}

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent Club/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_signup_for_activity_already_signed_up():
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Already signed up for this activity"}

def test_add_activity_success():
    response = client.post("/activities/add", json={
        "name": "Photography Club",
        "description": "Learn photography techniques and take amazing pictures",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 10
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Activity Photography Club added successfully"}

def test_add_activity_already_exists():
    response = client.post("/activities/add", json={
        "name": "Chess Club",
        "description": "Duplicate activity",
        "schedule": "Mondays, 10:00 AM - 12:00 PM",
        "max_participants": 5
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Activity already exists"}