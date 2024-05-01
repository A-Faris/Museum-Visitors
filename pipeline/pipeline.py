"""Functions that interact with the database."""

import csv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from extract import path, BUCKET_FOLDER, MERGE_CSV_FILE


def get_db_connection(dbname="museum") -> connection:
    """Returns a DB connection"""
    return connect(dbname=dbname,
                   cursor_factory=RealDictCursor)


def import_to_request(site: str, type: str, at: str) -> None:
    """Get subject info"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO request(exhibition_id, assistance_id , created_at)
        VALUES (%s, %s, %s)""", (site, int(float(type)), at))

    conn.commit()
    cur.close()


def import_to_review(site: str, val: str, at: str) -> None:
    """Get subject info"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO review(exhibition_id, rating_id, created_at)
        VALUES (%s, %s, %s)""", (site, val, at))

    conn.commit()
    cur.close()


if __name__ == "__main__":
    file = path(MERGE_CSV_FILE, BUCKET_FOLDER)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type']:
                import_to_request(row['site'], row['type'], row['at'])
            else:
                import_to_review(row['site'], row['val'], row['at'])
            print(row['at'], row['site'], row['val'], row['type'])
