"""
Pytest configuration and fixtures for test suite
"""

import pytest
from src.app import activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and training",
            "schedule": "Tuesday and Thursday, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis instruction and friendly matches",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and various art techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions and acting workshops",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific experiments and research projects",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Clear all participants
    for activity_name in activities:
        activities[activity_name]["participants"].clear()
    
    # Restore original participants
    for activity_name, activity_data in original_activities.items():
        activities[activity_name]["participants"] = activity_data["participants"].copy()
    
    yield
    
    # Reset after test
    for activity_name in activities:
        activities[activity_name]["participants"].clear()
    for activity_name, activity_data in original_activities.items():
        activities[activity_name]["participants"] = activity_data["participants"].copy()
