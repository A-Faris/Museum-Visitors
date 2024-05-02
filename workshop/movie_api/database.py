"""Database for Movie API"""
# pylint: skip-file

from typing import Any
from os import environ
from datetime import date
import psycopg2.extras
from psycopg2.extensions import connection, cursor
from dotenv import load_dotenv
from import_movie import import_movies_to_database, get_id


def get_connection() -> connection:
    """Get Connection"""
    load_dotenv()
    return psycopg2.connect(
        user=environ["DATABASE_USERNAME"],
        password=environ["DATABASE_PASSWORD"],
        host=environ["DATABASE_IP"],
        port=environ["DATABASE_PORT"],
        database=environ["DATABASE_NAME"]
    )


def get_cursor(conn: connection) -> cursor:
    """Get Cursor"""
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def get_movies(search: str | None,
               sort_by: str | None = None,
               sort_order: str | None = None) -> list[dict] | list:
    """Get movies"""
    # Example implementation
    conn = get_connection()
    cur = get_cursor(conn)

    query = "SELECT * FROM movies "
    if search:
        query += "WHERE title LIKE %s "
        if sort_by:
            query += f"ORDER BY {sort_by} {sort_order}"

    cur.execute(query, (f"%{search}%",))

    data = cur.fetchall()
    conn.commit()
    cur.close()
    # Return list of movies
    return data


def get_movie_by_id(movie_id: int) -> dict[str, Any]:
    """Get movie by ID"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute("""SELECT * FROM movies
                    WHERE movie_id = %s""", (movie_id,))

    data = cur.fetchone()
    conn.commit()
    cur.close()
    return data


def create_movie(title: str, release_date: date, genre: str, actors: list[str], overview: str,
                 status: str, budget: int, revenue: int, country: str, language: str) -> dict:
    """Create movie"""
    data = import_movies_to_database([{"title": title,
                                       "release_date": release_date,
                                       "score": 10,
                                       "genre": genre,
                                       "overview": overview,
                                       "crew": actors,
                                       "orig_title": "jhj",
                                       "status": status,
                                       "language": language,
                                       "budget": budget,
                                       "revenue": revenue,
                                       "country": country}])
    return data[-1]


def update_movie(title: str, release_date: date, genre: str, actors: list[str],
                 overview: str, status: str, budget: int, revenue: int,
                 country: str, language: str, movie_id: int) -> dict[str, Any]:
    """Update movie"""
    conn = get_connection()
    cur = get_cursor(conn)

    language_id = get_id(
        cur, language, "languages", "language", "language_id")

    country_id = get_id(
        cur, country, "countries", "country", "country_id")

    attributes = {"title": title,
                  "release_date": release_date,
                  "overview": overview,
                  "status": status,
                  "language_id": language_id,
                  "budget": budget,
                  "revenue": revenue,
                  "country_id": country_id}

    for word, attribute in attributes.items():
        if attribute:
            cur.execute(f"""UPDATE movies
                        SET {word} = %s
                        WHERE movie_id = %s; """,
                        (attribute, movie_id))

    genre_id = get_id(cur, genre, "genres", "genre", "genre_id")

    cur.execute(
        """UPDATE genre_assignment
        SET genre_id = %s
        WHERE movie_id = %s; """,
        (genre_id, movie_id))

    actor_ids = [get_id(cur, actor, "actors", "actor", "actor_id")
                 for actor in actors[::2]]

    role_ids = [get_id(cur, role, "roles", "role", "role_id")
                for role in actors[1::2]]

    for actor_id, role_id in zip(actor_ids, role_ids):
        cur.execute(
            """UPDATE crew_assignment
            SET actor_id = %s,
            role_id = %s
            WHERE movie_id = %s; """,
            (actor_id, role_id, movie_id))

    cur.execute(
        """SELECT * FROM movies
        WHERE movie_id = %s; """,
        (movie_id,))

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def delete_movie(movie_id: int) -> bool:
    """Delete movie"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """DELETE FROM movies
            WHERE movie_id = %s; """, (movie_id,))

    data = cur.fetchone()
    conn.commit()
    cur.close()
    return data is not None


def get_genres() -> list[dict[str, str]] | list:
    """Get genres"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute("SELECT * FROM genres")

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_genre(genre_id: int) -> dict:
    """Get genre"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(f"""SELECT genre FROM genres
                WHERE genre_id = {genre_id}""")

    data = cur.fetchone()
    conn.commit()
    cur.close()
    return data


def get_movies_by_genre(genre_id: int) -> list[dict[str, Any]]:
    """Get movies by genre"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute("""SELECT * FROM movies
                JOIN genre_assignment USING(movie_id)
                WHERE genre_id = %s""",
                (genre_id,))

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def search_actor(search_term: str) -> list[str] | list:
    """Search actor"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute("""SELECT title FROM movies
                JOIN crew_assignment USING(movie_id)
                JOIN actors USING(actor_id)
                WHERE actor LIKE % s""",
                (f"%{search_term}%",))

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_movie_by_country(country_code, sort_by: str | None = None,
                         sort_order: str | None = None) -> list[dict] | list:
    """Get movie by country"""
    conn = get_connection()
    cur = get_cursor(conn)

    query = """SELECT * FROM movies
            JOIN countries USING(country_id)
            WHERE country = %s """
    if sort_by:
        query += f"ORDER BY {sort_by} {sort_order}"

    cur.execute(query, (country_code,))

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def get_countries() -> list[str]:
    """Get countries"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute("SELECT country FROM countries")

    datas = cur.fetchall()
    conn.commit()
    cur.close()
    return [data["country"] for data in datas]
