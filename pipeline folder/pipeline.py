"""Functions that interact with the database."""

import logging
import csv
import time
import argparse
from os import environ
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection
from extract import BUCKET_FOLDER, MERGE_CSV_FILE, BUCKET_NAME, \
    path, get_client, find_file_paths, create_folder, download_bucket, \
    dotenv_values, combine_csv_files, delete_files, bucket_names

LOG_FOLDER = "logs"


def log_to_file(file_name: str, folder: str = LOG_FOLDER) -> None:
    create_folder(folder)
    logging.basicConfig(filename=path(f'{file_name}_{(time.time())}.log', folder),
                        encoding='utf-8',
                        level=logging.INFO,
                        filemode='w')


def get_db_connection() -> connection:
    """Get connection"""
    load_dotenv()
    return connect(
        user=environ["DATABASE_USERNAME"],
        password=environ["DATABASE_PASSWORD"],
        host=environ["DATABASE_IP"],
        port=environ["DATABASE_PORT"],
        database=environ["DATABASE_NAME"]
    )


def import_to_request(site: str, type_db: str, at: str) -> None:
    """Import into table request"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO request(exhibition_id, assistance_id, created_at)
        VALUES (%s::INT, %s::INT, %s::TIMESTAMP)""", (site, float(type_db), at))

    conn.commit()
    cur.close()


def import_to_review(site: str, val: str, at: str) -> None:
    """Import into table review"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """INSERT INTO review(exhibition_id, rating_id, created_at)
        VALUES (%s::INT, %s::INT, %s::TIMESTAMP)""", (site, val, at))

    conn.commit()
    cur.close()
    logging.info("All files downloaded.")


def import_to_database(csv_file: str, folder: str, limit: int = None):
    """Import csv file into the RDS database"""
    file = path(csv_file, folder)
    with open(file, newline='', encoding="utf-8") as csvfile:
        if limit:
            csvfile = [next(csvfile) for _ in range(limit)]
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type']:
                import_to_request(row['site'], row['type'],
                                  row['at'])
                logging.info("csv data imported to request.")
            else:
                import_to_review(row['site'], row['val'],
                                 row['at'])
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
                        help="Choose name of csv file to store the data. 'lmnh_hist_data.csv'.")
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
        logger = log_to_file("pipeline")

    else:
        logging.basicConfig(level=logging.INFO)

    create_folder(args.folder)
    download_bucket(clients, args.bucket, args.folder)

    csv_files = find_file_paths('csv', args.folder)
    combine_csv_files(csv_files, args.csv_file, args.folder)
    delete_files(csv_files, args.csv_file, args.folder)

    import_to_database(args.csv_file, args.folder, args.num_of_rows)
