"""Extract file"""

import argparse
from os import mkdir, remove, path, environ
import re
import glob
# import json

from boto3 import client
from dotenv import load_dotenv
import pandas as pd  # csv

BUCKET_FOLDER = "buckets"
BUCKET_NAME = "sigma-resources-museum"
USEFUL_FILES = "^lmnh.*.(csv|json)$"
MERGE_CSV_FILE = 'lmnh_hist_data.csv'


def create_folder(folder: str) -> None:
    """Create a folder to store data"""
    if folder and not path.exists(folder):
        mkdir(folder)


def bucket_names(sss) -> list:
    """Print out bucket names"""
    buckets = sss.list_buckets()["Buckets"]
    return [bucket["Name"] for bucket in buckets]


def download_bucket(sss, bucket_name: str, folder=".") -> None:
    """Download the bucket contents"""
    bucket = sss.list_objects(Bucket=bucket_name)
    for file in bucket["Contents"]:
        if re.search(USEFUL_FILES, file["Key"]):
            sss.download_file(
                bucket_name, file["Key"], path.join(folder, file["Key"]))


def find_file_paths(file_format: str = "", folder: str = ".") -> list[str]:
    "Return the file paths of a file format"
    return list(glob.iglob(f'*.{file_format}', root_dir=folder))


def combine_csv_files(csv_files: list, merge_file_name: str, folder: str = ".") -> None:
    """Combine multiple csv files into one csv file"""
    combined_file = pd.concat([pd.read_csv(path.join(folder, file)) for file in csv_files
                              if merge_file_name not in file])

    combined_file.to_csv(path.join(folder, merge_file_name), index=False)


def delete_files(files: list, exception: str = None, folder: str = ".") -> list[None]:
    """Delete files in folder"""
    if exception in files:
        files.remove(exception)
    return [remove(path.join(folder, file)) for file in files if path.exists(path.join(folder, file))]

# def combine_json_files(read_files: list, merge_file_name: str, folder: str = ".") -> None:
#     textfile_merged = open(merge_file_name, 'w')

#     for f in read_files:
#         with open(f, 'w+t') as file:
#             data = json.load(file)
#             json.dump(data, merge_file_name)

#     textfile_merged.close()


if __name__ == '__main__':
    load_dotenv()
    clients = client("s3", aws_access_key_id=environ["ACCESS_KEY"],
                     aws_secret_access_key=environ["SECRET_ACCESS_KEY"])

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", "-b",
                        choices=bucket_names(clients),
                        default=BUCKET_NAME,
                        help="Choose bucket name to download")
    parser.add_argument("--folder", "-f",
                        default=BUCKET_FOLDER,
                        help="Choose bucket folder to store the data")
    parser.add_argument("--num_of_rows", "-r",
                        help="Choose number of rows to upload to the database",
                        type=int)
    parser.add_argument("--log_file", "-l",
                        default=False,
                        help="Choose to log to a file or to the terminal",
                        type=int)
    args = parser.parse_args()
    create_folder(args.folder)
    download_bucket(clients, args.bucket, args.folder)

    csv_files = find_file_paths('csv', args.folder)
    combine_csv_files(csv_files, MERGE_CSV_FILE, args.folder)
    delete_files(csv_files, MERGE_CSV_FILE, args.folder)

    # json_files = find_files('.json', BUCKET_FOLDER)
    # combine_json_files(json_files, 'lmnh_exhibition_data.json', BUCKET_FOLDER)
    # delete_files(json_files)
