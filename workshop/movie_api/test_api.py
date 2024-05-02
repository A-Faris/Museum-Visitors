# pylint: skip-file


import pytest
from flask import json
from datetime import datetime
from api import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_endpoint_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Movie API"}


def test_endpoint_get_movies(client):
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_endpoint_get_movie(client):
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert isinstance(response.json, dict)


@patch('api.get_connection')
def test_endpoint_create_movie(client):
    data = {
        "title": "Test Movie",
        "release_date": "01/01/2022",
        "genre": "Action",
        "actors": ["Actor 1", "Actor 2"]
    }
    response = client.post("/movies", json=data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_endpoint_delete_movie(client):
    response = client.delete("/movies/1")
    assert response.status_code == 200
    assert response.json == {"message": "Movie deleted"}


def test_endpoint_get_genres(client):
    response = client.get("/genres")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_endpoint_movies_by_genre(client):
    response = client.get("/genres/1/movies")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_endpoint_search_actor(client):
    response = client.get("/actors?search=Actor")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_endpoint_get_movies_by_country(client):
    response = client.get("/countries/US")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_invalid_sort_by(client):
    response = client.get("/movies?sort_by=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_by parameter"}


def test_invalid_sort_order(client):
    response = client.get("/movies?sort_order=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_order parameter"}


def test_missing_required_fields(client):
    data = {
        "title": "Test Movie",
        "genre": "Action",
        "actors": ["Actor 1", "Actor 2"]
    }
    response = client.post("/movies", json=data)
    assert response.status_code == 400
    assert response.json == {"error": "Missing required fields"}


def test_invalid_release_date_format(client):
    data = {
        "title": "Test Movie",
        "release_date": "2022-01-01",
        "genre": "Action",
        "actors": ["Actor 1", "Actor 2"]
    }
    response = client.post("/movies", json=data)
    assert response.status_code == 400
    assert response.json == {
        "error": "Invalid release_date format. Please use MM/DD/YYYY"}


def test_movie_not_found(client):
    response = client.get("/movies/999999")
    assert response.status_code == 404
    assert response.json == {"error": "Movie not found"}


def test_genre_not_found(client):
    response = client.get("/genres/999/movies")
    assert response.status_code == 404
    assert response.json == {"error": "Genre not found"}


def test_no_movies_found(client):
    response = client.get("/movies?search=Nonexistent")
    assert response.status_code == 404
    assert response.json == {"error": "No movies found"}


def test_no_genres_found(client):
    response = client.get("/genres")
    assert response.status_code == 404
    assert response.json == {"error": "No genres found"}


def test_no_actors_found(client):
    response = client.get("/actors?search=Nonexistent")
    assert response.status_code == 404
    assert response.json == {"error": "No actors found"}


def test_country_not_found(client):
    response = client.get("/countries/ZZ")
    assert response.status_code == 404
    assert response.json == {"error": "Country not found"}


def test_invalid_sort_by_parameter(client):
    response = client.get("/countries/US?sort_by=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_by parameter"}


def test_invalid_sort_order_parameter(client):
    response = client.get("/countries/US?sort_order=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_order parameter"}


@patch('database.get_connection')
def test_endpoint_update_movie(client):
    response = client.put(
        "/movies/1", json={"title": "New Title", "release_date": "2022-12-31", "genre": "Action"})
    assert response.status_code == 200
    assert response.json == {"message": "Movie updated successfully"}


def test_endpoint_search_movie(client):
    response = client.get("/movies?search=Creed")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Creed III"


def test_endpoint_get_movie_actors(client):
    response = client.get("/movies/1/actors")
    assert response.status_code == 200
    assert len(response.json) == 17
    assert response.json[0]["name"] == "Michael B. Jordan"


def test_endpoint_get_countries(client):
    response = client.get("/countries")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0] == "AU"


def test_endpoint_validate_sort_by(client):
    response = client.get("/movies?sort_by=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_by parameter"}


def test_endpoint_validate_sort_order(client):
    response = client.get("/movies?sort_order=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_order parameter"}


def test_endpoint_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Movie API"}


@patch('database.get_connection')
def test_endpoint_create_movie(client):
    response = client.post(
        "/movies", json={"title": "New Movie", "release_date": "2022-01-01", "genre": "Comedy"})
    assert response.status_code == 201
    assert response.json == {"message": "Movie created successfully"}


def test_endpoint_delete_movie(client):
    response = client.delete("/movies/1")
    assert response.status_code == 200
    assert response.json == {"message": "Movie deleted successfully"}


def test_endpoint_get_genres(client):
    response = client.get("/genres")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0] == "Drama"
    assert response.json[1] == "Action"


def test_endpoint_movies_by_genre(client):
    response = client.get("/genres/1/movies")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Creed III"


def test_endpoint_search_actor(client):
    response = client.get("/actors?search=Michael B. Jordan")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Michael B. Jordan"


def test_endpoint_get_movies_by_country(client):
    response = client.get("/countries/AU")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Creed III"
    assert response.json[0]["country"] == "AU"


def test_endpoint_get_movies_by_country_with_sort(client):
    response = client.get("/countries/AU?sort_by=title&sort_order=asc")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Creed III"
    assert response.json[0]["country"] == "AU"


def test_endpoint_get_movies_by_country_with_invalid_sort(client):
    response = client.get("/countries/AU?sort_by=invalid&sort_order=asc")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_by parameter"}


def test_endpoint_get_movies_by_country_with_invalid_sort_order(client):
    response = client.get("/countries/AU?sort_by=title&sort_order=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_order parameter"}


def test_endpoint_get_movies_by_country_with_no_movies(client):
    response = client.get("/countries/US")
    assert response.status_code == 404
    assert response.json == {"error": "No movies found for the country"}


def test_endpoint_get_movies_by_country_with_no_genres(client):
    response = client.get("/countries/UK")
    assert response.status_code == 404
    assert response.json == {"error": "No genres found for the country"}


def test_endpoint_get_movies_by_country_with_no_actors(client):
    response = client.get("/countries/CA")
    assert response.status_code == 404
    assert response.json == {"error": "No actors found for the country"}


def test_endpoint_search_movie_with_no_results(client):
    response = client.get("/movies?search=Avengers")
    assert response.status_code == 404
    assert response.json == {"error": "No movies found"}


def test_endpoint_get_movie_actors_with_no_results(client):
    response = client.get("/movies/2/actors")
    assert response.status_code == 404
    assert response.json == {"error": "No actors found for the movie"}


def test_endpoint_get_countries(client):
    response = client.get("/countries")
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[0] == "AU"
    assert response.json[1] == "US"
    assert response.json[2] == "UK"


def test_endpoint_validate_sort_by(client):
    response = client.get("/movies?sort_by=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_by parameter"}


def test_endpoint_validate_sort_order(client):
    response = client.get("/movies?sort_order=invalid")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid sort_order parameter"}


def test_endpoint_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Movie API"}
