"""Tests for the API routes."""

# pylint: skip-file

from unittest.mock import patch
from datetime import date

import pytest
from psycopg2 import connect


class TestSubjectRoute:
    """Tests for the /subject route."""

    def test_returns_200_on_GET(self, test_api):
        """Checks that the route accepts a GET request."""

        res = test_api.get("/subject")

        assert res.status_code == 200

    def test_returns_list_of_valid_dicts(self, test_api):
        """Checks that the route returns data in the right format."""

        res = test_api.get("/subject")

        required_keys = ["subject_id", "subject_name",
                         "species_name", "date_of_birth"]

        data = res.json

        assert isinstance(data, list), "Not a list"
        assert all(isinstance(d, dict) for d in data), "Not a list of dicts"
        assert all(len(d.keys()) == len(required_keys)
                   for d in data), "Wrong number of keys"
        for k in required_keys:
            assert all(k in d for d in data), f"Key ({k}) not found in data"

    def test_returns_expected_data(self, test_api, example_subjects):
        """Checks that the expected data is returned."""

        res = test_api.get("/subject")

        data = res.json

        assert len(data) == 5

        for i in range(len(data)):
            assert data[i] == example_subjects[i]


class TestExperimentRoute:
    """Tests for the /experiment route."""

    def test_returns_200_on_GET(self, test_api):
        """Checks that the route accepts a GET request."""

        res = test_api.get("/experiment")

        assert res.status_code == 200

    def test_returns_list_of_valid_dicts(self, test_api):
        """Checks that the route returns data in the right format."""

        res = test_api.get("/experiment")

        required_keys = ["experiment_date", "experiment_id",
                         "experiment_type", "score",
                         "species", "subject_id"]

        data = res.json

        assert isinstance(data, list), "Not a list"
        assert all(isinstance(d, dict) for d in data), "Not a list of dicts"
        assert all(len(d.keys()) == len(required_keys)
                   for d in data), "Wrong number of keys"
        for k in required_keys:
            assert all(k in d for d in data), f"Key ({k}) not found in data"

    def test_returns_expected_data(self, test_api, example_experiments):
        """Checks that the expected data is returned."""

        res = test_api.get("/experiment")

        data = res.json

        assert len(data) == 10

        for i in range(len(data)):
            assert data[i] == example_experiments[i]

    @pytest.mark.parametrize("filter_score,output", ((90, 2), (80, 4), (50, 7), (1, 10)))
    def test_returns_expected_data_when_score_is_filtered(self, filter_score, output, test_api):
        """Checks that non-matching values are filtered out."""

        res = test_api.get(f"/experiment?score_over={filter_score}")

        data = res.json

        assert len(data) == output

        for d in data:
            assert float(d["score"][:-1]) >= filter_score

    @pytest.mark.parametrize("filter_type,output", (("intelligence", 5), ("obedience", 3), ("aggression", 2)))
    def test_returns_expected_data_when_type_is_filtered(self, filter_type, output, test_api):
        """Checks that non-matching values are filtered out."""

        res = test_api.get(f"/experiment?type={filter_type}")

        data = res.json

        assert len(data) == output

        for d in data:
            assert d["experiment_type"] == filter_type

    @pytest.mark.parametrize("filter_type, filter_score,output", (("obedience", 90, 0), ("intelligence", 50, 4), ("aggression", 2, 2)))
    def test_returns_expected_data_when_type_and_score_filtered(self, filter_type, filter_score, output, test_api):
        """Checks that non-matching values are filtered out."""

        res = test_api.get(
            f"/experiment?type={filter_type}&score_over={filter_score}")

        data = res.json

        assert len(data) == output

        for d in data:
            assert d["experiment_type"] == filter_type
            assert float(d["score"][:-1]) >= filter_score


class TestExperimentIDRoute:
    """Tests for the /experiment/<id> route."""

    def test_accepts_on_DELETE(self, test_api):
        """Checks that the route accepts a DELETE request."""

        res = test_api.delete("/experiment/3")

        assert res.status_code != 405

    @pytest.mark.parametrize("id", (3000, 26, 35, 100, 9241))
    def test_rejects_invalid_id(self, id, test_api):
        """Checks that the route rejects an invalid ID."""

        print(f"/experiment/{id}")
        res = test_api.delete(f"/experiment/{id}")

        data = res.json

        assert res.status_code == 404
        assert isinstance(data, dict)

    @pytest.mark.parametrize("id, exp_date", ((1, "2024-01-06"), (3, "2024-01-06"), (5, "2024-01-06"),
                                              (2, "2024-01-06"), (8, "2024-02-06")))
    def test_deletes_on_valid_id(self, id, exp_date, test_api, test_temp_conn):
        """Checks that the route deletes valid IDs."""

        res = test_api.delete(f"/experiment/{id}")
        data = res.json

        assert res.status_code == 200
        assert isinstance(data, dict)
        assert "experiment_id" in data
        assert "experiment_date" in data
        assert exp_date == data["experiment_date"]

        with test_temp_conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM experiment WHERE experiment_id = %s", [id])
            data = cur.fetchall()

        assert not data, "Failed to actually delete the row"
