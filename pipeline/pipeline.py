"""Functions that interact with the database."""

import psycopg2.extras
from dotenv import load_dotenv
from os import environ
import logging
import csv
import time
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from extract import *

LOG_FOLDER = "logs"


def get_db_connection() -> connection:
    """Get connection"""
    load_dotenv()
    return psycopg2.connect(
        user=environ["DATABASE_USERNAME"],
        password=environ["DATABASE_PASSWORD"],
        host=environ["DATABASE_IP"],
        port=environ["DATABASE_PORT"],
        database=environ["DATABASE_NAME"]
    )


def import_to_request(site: str, type: str, at: str, limit: int = 0) -> None:
    """Import into table request"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO request(exhibition_id, assistance_id, created_at)
        VALUES (%s::INT, %s::INT, %s::TIMESTAMP)""", (site, float(type), at, limit))

    conn.commit()
    cur.close()


def import_to_review(site: str, val: str, at: str, limit: int = 0) -> None:
    """Import into table review"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO review(exhibition_id, rating_id, created_at)
        VALUES (%s::INT, %s::INT, %s::TIMESTAMP)""", (site, val, at, limit))

    conn.commit()
    cur.close()


def import_to_database(csv_file: str, folder: str):
    file = path(csv_file, folder)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type']:
                import_to_request(row['site'], row['type'],
                                  row['at'], args.num_of_rows)
                logging.info("csv data imported to request.")
            else:
                import_to_review(row['site'], row['val'],
                                 row['at'], args.num_of_rows)
                logging.info("csv data imported to review.")
        logging.info("All files downloaded.")


if __name__ == "__main__":
    clients = get_client(dotenv_values().get("ACCESS_KEY"),
                         dotenv_values().get("SECRET_ACCESS_KEY"))

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", "-b",
                        choices=bucket_names(clients),
                        default=BUCKET_NAME,
                        help="Choose bucket name to download. Default 'sigma-resources-museum'.")
    parser.add_argument("--folder", "-f",
                        default=BUCKET_FOLDER,
                        help="Choose bucket folder to store the data. Default 'buckets'.")
    parser.add_argument("--csv_file", "-c",
                        default=MERGE_CSV_FILE,
                        help="Choose name of csv file to store the data. Default 'lmnh_hist_data.csv'.")
    parser.add_argument("--num_of_rows", "-r",
                        help="Choose number of rows to upload to the database",
                        type=int)
    parser.add_argument("--log", "-l",
                        default=True,
                        help="Choose to log to a file or to the terminal. Default 'True'.",
                        type=bool)
    args = parser.parse_args()
    print(args)

    if args.log:
        create_folder(LOG_FOLDER)
        logging.basicConfig(filename=path(f'pipeline_{(time.time())}.log', LOG_FOLDER),
                            encoding='utf-8', level=logging.INFO, filemode='w')
    else:
        logging.basicConfig(level=logging.INFO)

    create_folder(args.folder)
    download_bucket(clients, args.bucket, args.folder)

    csv_files = find_file_paths('csv', args.folder)
    combine_csv_files(csv_files, args.csv_file, args.folder)
    delete_files(csv_files, args.csv_file, args.folder)

    import_to_database(args.csv_file, args.folder)
