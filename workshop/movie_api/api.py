"""Movie API"""

from datetime import datetime
from flask import Flask, jsonify, request
from database import (
    get_movies,
    get_movie_by_id,
    create_movie,
    update_movie,
    delete_movie,
    get_genres,
    get_genre,
    get_movies_by_genre,
    search_actor,
    get_movie_by_country,
    get_countries
)

# Note from the Movie DB API team: This half-finished code was written by an intern
# with no coding experience so expect there to be bugs and issues.
# Please review the code and make any necessary changes to ensure it's production-ready. Good luck!

app = Flask(__name__)


def validate_sort_by(sort_by: str | None) -> bool:
    """Validate sort by"""
    return sort_by in ["title", "release_date", "genre", "revenue", "budget", "score", None]


def validate_sort_order(sort_order: str) -> bool:
    """Validate sort order"""
    return sort_order in ["asc", "desc"]


@app.route("/", methods=["GET"])
def endpoint_index():
    """Endpoint index"""
    return jsonify({"message": "Welcome to the Movie API"})


@app.route("/movies", methods=["GET"])
def endpoint_get_movies():
    """Endpoint get movies"""
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", "asc")
    search = request.args.get("search")

    if not validate_sort_by(sort_by):
        return jsonify({"error": "Invalid sort_by parameter"}), 400

    if not validate_sort_order(sort_order):
        return jsonify({"error": "Invalid sort_order parameter"}), 400

    movies = get_movies(search, sort_by, sort_order)

    if not movies:
        return jsonify({"error": "No movies found"}), 404

    return jsonify(movies), 200


@app.route("/movies", methods=["POST"])
def endpoint_post_movies():
    """Endpoint post movies"""
    data = request.get_json
    title = data.get["title"]
    release_date = data.get["release_date"]
    genre = data.get["genre"]
    actors = data.get("actors", [])
    overview: str = data.get("overview", "")
    status = data.get("status", "released")
    budget: int = data.get("budget", 0)
    revenue: int = data.get("revenue", 0)
    country: str = data.get("country")
    language: str = data.get("language")

    if not any([title, release_date, genre, country, language, actors]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        datetime.strptime(release_date, "%m/%d/%Y")
    except ValueError:
        return jsonify({"error": "Invalid release_date format. Please use MM/DD/YYYY"}), 400

    try:
        movie = create_movie(title, release_date, genre, actors, overview,
                             status, budget, revenue, country, language)
        return jsonify({"message": "Movie created successfully",
                        'success': True,
                        "movie": movie}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/movies/<int:movie_id>", methods=["PATCH"])
def endpoint_patch_movie(movie_id: int):
    """Endpoint patch movie"""
    data = request.get_json
    title = data.get("title")
    release_date = data.get("release_date")
    genre = data.get("genre")
    actors = data.get("actors")
    overview = data.get("overview")
    status = data.get("status")
    budget = data.get("budget")
    revenue = data.get("revenue")
    country = data.get("country")
    language = data.get("language")

    if not all([title, release_date, genre, actors, overview,
                status, budget, revenue, country, language]):
        return jsonify({"error": "No fields to update"}), 400

    try:
        movie = update_movie(title, release_date, genre, actors,
                             overview, status, budget, revenue, country, language, movie_id)
        return jsonify({'success': True, "movie": movie}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/movies/<int:movie_id>", methods=["GET"])
def endpoint_get_movie(movie_id: int):
    """Endpoint get movie"""
    movie = get_movie_by_id(movie_id)

    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify(movie), 200


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def endpoint_delete_movie(movie_id: int):
    """Endpoint delete movie"""
    success = delete_movie(movie_id)

    if not success:
        return jsonify({"error": "Movie could not be deleted"}), 404

    return jsonify({"message": "Movie deleted"})


@app.route("/genres", methods=["GET"])
def endpoint_get_genres():
    """Get a list of all genres"""
    genres = get_genres()

    if not genres:
        return jsonify({"error": "No genres found"}), 404

    return jsonify(genres)


@app.route("/genres/<int:genre_id>/movies", methods=["GET"])
def endpoint_movies_by_genre(genre_id: int):
    """Get list of movie details by genre"""

    if not get_genre(genre_id):
        return jsonify({"error": "Genre not found"}), 404

    movies = get_movies_by_genre(genre_id)

    if not movies:
        return jsonify({"error": "No movies found for this genre"}), 404

    return jsonify(movies)


@app.route("/actors", methods=["GET"])
def endpoint_search_actor():
    """Endpoint should return a list of actors based on the search term provided
    in the query string and all of the films each of them has appeared in."""
    search_term = request.args.get("search")

    if not search_term:
        return jsonify({"error": "Search term empty found"}), 404

    actors = search_actor(search_term)

    if not actors:
        return jsonify({"error": "No actors found"}), 404

    return jsonify(actors)


@app.route("/countries/<string:country_code>", methods=["GET"])
def endpoint_get_movies_by_country(country_code: str):
    """Get a list of movie details by country.
    Optionally, the results can be sorted by a specific field in ascending or descending order."""

    if country_code not in get_countries():
        return jsonify({"error": "Country not found"}), 404

    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order")

    if not validate_sort_by(sort_by):
        return jsonify({"error": "Invalid sort_by parameter"}), 400

    if not validate_sort_order(sort_order):
        return jsonify({"error": "Invalid sort_order parameter"}), 400

    movies = get_movie_by_country(country_code, sort_by, sort_order)

    if not movies:
        return jsonify({"error": "No movies found for this country"}), 404

    return jsonify(movies)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
