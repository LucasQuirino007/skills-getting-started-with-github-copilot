"""Tests for the activity unregister endpoint."""


class TestUnregisterFromActivity:
    def test_unregister_removes_student_from_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already signed up in seed data

        # Act
        response = client.request(
            "DELETE", f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "message": f"Unregistered {email} from {activity_name}"
        }
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity_name]["participants"]

    def test_unregister_for_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "michael@mergington.edu"

        # Act
        response = client.request(
            "DELETE", f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_when_not_registered_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.request(
            "DELETE", f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert (
            response.json()["detail"] == "Student is not signed up for this activity"
        )
