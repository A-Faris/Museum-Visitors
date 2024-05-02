"""Tests for the API routes."""

# pylint: skip-file


class TestPostExperimentRoute:
    """Tests for the /experiment route."""

    def test_accepts_on_POST(self, test_api):
        """Checks that the route accepts a POST request."""

        data = {
            "subject_id": 3,
            "experiment_type": "obedience",
            "experiment_date": "2024-03-01",
            "score": 7
        }

        res = test_api.post("/experiment", json=data)

        assert res.status_code == 201

    def test_rejects_invalid_experiment_type(self, test_api):
        """Checks that the route rejects an invalid experiment type."""

        data = {
            "subject_id": 3,
            "experiment_type": "reject",
            "experiment_date": "2024-03-01",
            "score": 7
        }

        res = test_api.post("/experiment", json=data)

        assert res.status_code == 400

    def test_rejects_invalid_greater_score(self, test_api):
        """Checks that the route rejects an invalid score higher than maximum score"""

        data = {
            "subject_id": 3,
            "experiment_type": "obedience",
            "experiment_date": "2024-03-01",
            "score": 15
        }

        res = test_api.post("/experiment", json=data)

        assert res.status_code == 400
