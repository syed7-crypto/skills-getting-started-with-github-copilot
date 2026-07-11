import src.app as app_module


def test_get_activities_returns_seeded_data(client):
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Drama Club",
        "Debate Team",
        "Science Olympiad",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_activity_names
    assert activities["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert activities["Science Olympiad"]["participants"] == ["mia@mergington.edu"]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_participant = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_participant},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_participant} for {activity_name}"}
    assert new_participant in app_module.activities[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_participant = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_participant},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    missing_activity = "Robotics Club"

    # Act
    response = client.post(
        f"/activities/{missing_activity}/signup",
        params={"email": "robot@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    participant = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": participant},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {participant} from {activity_name}"}


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    missing_participant = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": missing_participant},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}


def test_remove_participant_from_missing_activity_returns_404(client):
    # Arrange
    missing_activity = "Robotics Club"

    # Act
    response = client.delete(
        f"/activities/{missing_activity}/participants",
        params={"email": "robot@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}