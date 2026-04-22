"""
Tests for Mergington High School Management System API

Tests cover all endpoints:
- GET /activities: List all activities
- GET /: Redirect to static index
- POST /activities/{activity_name}/signup: Register for activity
- POST /activities/{activity_name}/unregister: Unregister from activity
"""

import pytest
from starlette.testclient import TestClient
from src.app import app

# Create a test client
client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_200(self):
        """Verify GET /activities returns 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_list(self):
        """Verify GET /activities returns a list"""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_activities(self):
        """Verify response contains expected activities"""
        response = client.get("/activities")
        data = response.json()
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Drama Club",
            "Science Club",
            "Debate Team"
        ]
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_has_required_fields(self):
        """Verify each activity has required fields"""
        response = client.get("/activities")
        data = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Activity {activity_name} missing field {field}"

    def test_get_activities_correct_count(self):
        """Verify correct number of activities (should be 9)"""
        response = client.get("/activities")
        data = response.json()
        assert len(data) == 9


class TestRootRedirect:
    """Tests for GET / endpoint"""

    def test_root_redirect_status(self):
        """Verify GET / returns 307 redirect status"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307

    def test_root_redirect_location(self):
        """Verify GET / redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert "location" in response.headers
        assert response.headers["location"].endswith("/static/index.html")


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    @pytest.mark.parametrize("activity_name,email,expected_status", [
        ("Chess Club", "newstudent@mergington.edu", 200),
        ("Programming Class", "alice@mergington.edu", 200),
        ("Science Club", "bob@example.com", 200),
    ])
    def test_signup_success(self, activity_name, email, expected_status):
        """Verify successful signup returns 200 status"""
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == expected_status

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "student1@mergington.edu"),
        ("Programming Class", "student2@mergington.edu"),
    ])
    def test_signup_success_contains_message(self, activity_name, email):
        """Verify successful signup response contains confirmation message"""
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        data = response.json()
        assert "message" in data

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "michael@mergington.edu"),  # Already registered
        ("Programming Class", "emma@mergington.edu"),
        ("Tennis Club", "james@mergington.edu"),
    ])
    def test_signup_duplicate_returns_400(self, activity_name, email):
        """Verify duplicate signup returns 400 error"""
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 400

    @pytest.mark.parametrize("invalid_activity", [
        "Nonexistent Club",
        "Invalid Activity",
        "Fake Club Name",
    ])
    def test_signup_invalid_activity_returns_404(self, invalid_activity):
        """Verify signup for nonexistent activity returns 404 error"""
        response = client.post(f"/activities/{invalid_activity}/signup", params={"email": "test@mergington.edu"})
        assert response.status_code == 404

    def test_signup_missing_email_parameter(self):
        """Verify signup without email parameter returns 422 validation error"""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == 422


class TestUnregister:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "michael@mergington.edu"),  # Already registered
        ("Programming Class", "emma@mergington.edu"),
        ("Science Club", "noah@mergington.edu"),
    ])
    def test_unregister_success(self, activity_name, email):
        """Verify successful unregister returns 200 status"""
        response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
        assert response.status_code == 200

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "michael@mergington.edu"),
        ("Drama Club", "lucas@mergington.edu"),
    ])
    def test_unregister_success_contains_message(self, activity_name, email):
        """Verify successful unregister response contains confirmation message"""
        response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
        data = response.json()
        assert "message" in data

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "notregistered@mergington.edu"),  # Not registered
        ("Programming Class", "alice@example.com"),
        ("Gym Class", "fake@mergington.edu"),
    ])
    def test_unregister_not_registered_returns_400(self, activity_name, email):
        """Verify unregister for non-registered user returns 400 error"""
        response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
        assert response.status_code == 400

    @pytest.mark.parametrize("invalid_activity", [
        "Nonexistent Club",
        "Invalid Activity",
        "Fake Club Name",
    ])
    def test_unregister_invalid_activity_returns_404(self, invalid_activity):
        """Verify unregister for nonexistent activity returns 404 error"""
        response = client.post(f"/activities/{invalid_activity}/unregister", params={"email": "test@mergington.edu"})
        assert response.status_code == 404

    def test_unregister_missing_email_parameter(self):
        """Verify unregister without email parameter returns 422 validation error"""
        response = client.post("/activities/Chess Club/unregister")
        assert response.status_code == 422
