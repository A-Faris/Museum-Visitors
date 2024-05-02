"""Tests for the API routes."""

# pylint: skip-file


class TestExperimentRoute:
    """Tests for the /experiment route."""

    def test_returns_400_on_invalid_type_GET(self, test_api):
        """A `GET` request to `/experiment` with an invalid value for the `type` parameter is rejected."""

        res = test_api.get("/experiment?type=trash")

        assert res.status_code == 400

    def test_returns_400_on_invalid_score_over_GET(self, test_api):
        """A `GET` request to `/experiment` with an invalid value for the `score_over` parameter is rejected."""

        res = test_api.get(f"/experiment?score_over=yo")

        assert res.status_code == 400
