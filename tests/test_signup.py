"""Tests for the activity signup endpoint."""


class TestSignupForActivity:
    def test_signup_adds_student_to_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "message": f"Signed up {email} for {activity_name}"
        }
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_when_already_registered_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already signed up in seed data

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "Student already signed up for this activity"
        )
