"""A script to import all of the movies in imdb_movies.csv into the database"""

import csv
from os import environ
from rich.progress import track
from dotenv import load_dotenv
import psycopg2.extras
from psycopg2.extensions import connection


def get_connection() -> connection:
    """Get connection"""
    load_dotenv()
    return psycopg2.connect(
        user=environ["DATABASE_USERNAME"],
        password=environ["DATABASE_PASSWORD"],
        host=environ["DATABASE_IP"],
        port=environ["DATABASE_PORT"],
        database=environ["DATABASE_NAME"]
    )


def load_csv(filename: str) -> list[dict]:
    """Load csv"""
    with open(filename, newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f, skipinitialspace=True))


def get_id(cur, value, table, attribute, table_id):
    """Add value to table and return the id"""
    cur.execute(f"""INSERT INTO {table} ({attribute})
                VALUES (%s)
                ON CONFLICT DO NOTHING""", (value.strip(),))

    cur.execute(f"""SELECT {table_id}
                FROM {table}
                WHERE {attribute} = %s""", (value.strip(),))

    return cur.fetchone()[table_id]


def get_movie_id(cur, title, date, score, overview, orig_title,
                 status, language_id, budget, revenue, country_id):
    """Get movie ID"""
    cur.execute(
        """INSERT INTO movies(title, release_date, score, overview,
        orig_title, status, language_id, budget, revenue, country_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING""", (title, date, score, overview, orig_title,
                                    status, language_id, budget, revenue, country_id)
    )

    cur.execute("""SELECT movie_id
                    FROM movies
                    WHERE title = %s""", (title,))

    return cur.fetchone()['movie_id']


def import_movies_to_database(movies: list[dict]):
    """Import movies to database"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    for movie in track(movies, description="Adding movies"):
        language_id = get_id(
            cur, movie["language"], "languages", "language", "language_id")

        country_id = get_id(
            cur, movie["country"], "countries", "country", "country_id")

        movie_id = get_movie_id(
            cur, movie["title"],
            movie["release_date"],
            movie["score"],
            movie["overview"],
            movie["orig_title"],
            movie["status"],
            language_id,
            movie["budget"],
            movie["revenue"],
            country_id)

        genres = movie["genre"].split(",")

        genre_ids = [get_id(cur, genre, "genres", "genre", "genre_id")
                     for genre in genres]

        for genre_id in genre_ids:
            cur.execute(
                f"""INSERT INTO genre_assignment(movie_id, genre_id)
                VALUES ({movie_id}, {genre_id})""")

        crew = movie["crew"].split(",")

        actor_ids = [get_id(cur, actor, "actors", "actor", "actor_id")
                     for actor in crew[::2]]

        role_ids = [get_id(cur, role, "roles", "role", "role_id")
                    for role in crew[1::2]]

        for actor_id, role_id in zip(actor_ids, role_ids):
            cur.execute(
                f"""INSERT INTO crew_assignment(movie_id, actor_id, role_id)
                VALUES ({movie_id}, {actor_id}, {role_id})""")

    conn.commit()

    cur.execute("SELECT * FROM movies")
    print(cur.fetchall())

    cur.close()
    conn.close()
    return movies


if __name__ == "__main__":
    load_movies = load_csv("imdb_movies.csv")
    import_movies_to_database(load_movies)
