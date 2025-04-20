import unittest
from fastapi.testclient import TestClient
from app import app, activities

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        # Mock activities data
        self.mock_activities = {
            "Chess Club": {
                "description": "Play chess with others",
                "schedule": "Fridays, 5:00 PM - 7:00 PM",
                "max_participants": 20,
                "participants": ["michael@mergington.edu"]
            }
        }
        # activities.clear()
        # activities.update(self.mock_activities)
        self.client = TestClient(app)

    def test_root_redirect(self):
        self.assertIn("Chess Club", self.mock_activities.keys())
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_get_activities(self):
        """Test retrieving the list of activities"""
        response = self.client.get("/activities")
        self.assertEqual(response.status_code, 200)
        activities = response.json()
        self.assertIsInstance(activities, dict)
        self.assertIn("Chess Club", activities)

    def test_signup_for_activity_success(self):
        """Test signing up for an activity successfully"""
        response = self.client.post("/activities/Chess Club/signup", params={"email": "newuser@mergington.edu"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Signed up newuser@mergington.edu for Chess Club"})

    def test_signup_for_activity_already_signed_up(self):
        """Test signing up for an activity when already signed up"""
        response = self.client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Already signed up for this activity"})

    def test_signup_for_activity_not_found(self):
        """Test signing up for a non-existent activity"""
        response = self.client.post("/activities/Nonexistent Club/signup", params={"email": "test@mergington.edu"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Activity not found"})

    def test_add_activity_success(self):
        """Test adding a new activity successfully"""
        response = self.client.post("/activities/add", json={
            "name": "Photography Club",
            "description": "Learn photography techniques",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Activity Photography Club added successfully"})

    def test_add_activity_already_exists(self):
        """Test adding an activity that already exists"""
        response = self.client.post("/activities/add", json={
            "name": "Chess Club",
            "description": "Duplicate activity",
            "schedule": "Mondays, 10:00 AM - 12:00 PM",
            "max_participants": 5
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Activity already exists"})

if __name__ == "__main__":
    unittest.main()