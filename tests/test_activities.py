"""Tests for the root and activity listing endpoints."""


class TestRootRedirect:
    def test_root_redirects_to_static_index(self, client):
        # Arrange
        # (no additional setup needed; client fixture provides a fresh app)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code in (302, 307)
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    def test_returns_all_activities(self, client):
        # Arrange
        expected_names = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Club",
            "Basketball Club",
            "Art Club",
            "Theater Club",
            "Science Club",
            "Debate Club",
        }

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert set(data.keys()) == expected_names

    def test_activity_contains_expected_fields(self, client):
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.get("/activities")

        # Assert
        activity = response.json()[activity_name]
        assert activity["description"]
        assert activity["schedule"]
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
        assert "michael@mergington.edu" in activity["participants"]
