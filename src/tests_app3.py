import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app

class TestHighSchoolAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_redirect(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_get_activities(self):
        response = self.client.get("/activities")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_signup_for_activity_success(self):
        with patch("app.activities", {
            "Test Club": {
                "description": "Test description",
                "schedule": "Test schedule",
                "max_participants": 10,
                "participants": []
            }
        }):
            response = self.client.post("/activities/Test Club/signup", params={"email": "test@mergington.edu"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Signed up test@mergington.edu for Test Club")

    def test_signup_for_activity_not_found(self):
        response = self.client.post("/activities/Nonexistent Club/signup", params={"email": "test@mergington.edu"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Activity not found")

    def test_signup_for_activity_already_signed_up(self):
        with patch("app.activities", {
            "Test Club": {
                "description": "Test description",
                "schedule": "Test schedule",
                "max_participants": 10,
                "participants": ["test@mergington.edu"]
            }
        }):
            response = self.client.post("/activities/Test Club/signup", params={"email": "test@mergington.edu"})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["detail"], "Already signed up for this activity")

    def test_add_activity_success(self):
        with patch("app.activities", {}):
            response = self.client.post("/activities/add", params={
                "name": "New Club",
                "description": "New description",
                "schedule": "New schedule",
                "max_participants": 15
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Activity New Club added successfully")

    def test_add_activity_already_exists(self):
        with patch("app.activities", {
            "Existing Club": {
                "description": "Existing description",
                "schedule": "Existing schedule",
                "max_participants": 10,
                "participants": []
            }
        }):
            response = self.client.post("/activities/add", params={
                "name": "Existing Club",
                "description": "New description",
                "schedule": "New schedule",
                "max_participants": 15
            })
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["detail"], "Activity already exists")

if __name__ == "__main__":
    unittest.main()