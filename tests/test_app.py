from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_returns_json(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity_returns_success(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    assert "message" in response.json()


def test_signup_for_activity_returns_conflict_when_already_signed_up(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_returns_success(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert "message" in response.json()