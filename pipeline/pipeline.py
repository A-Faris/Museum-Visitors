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


def import_to_request(csv_row) -> list:
    """Get subject info"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """""")

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


def import_to_review(csv_row) -> list:
    """Get subject info"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """""")

    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data


if __name__ == "__main__":
    file = path(MERGE_CSV_FILE, BUCKET_FOLDER)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type']:

            print(row['at'], row['site'], row['val'], row['type'])
