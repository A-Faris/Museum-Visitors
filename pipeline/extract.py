"""Extract file"""
import os
import re
import glob
# import json
from boto3 import client
from dotenv import dotenv_values
import pandas as pd  # csv

BUCKET_FOLDER = "buckets"
BUCKET_NAME = "sigma-resources-museum"
USEFUL_FILES = "^lmnh.*.(csv|json)$"
MERGE_CSV_FILE = 'lmnh_hist_data.csv'


def get_client(access_key, secret_access_key):
    """Returns the s3 client"""
    return client('s3', aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key)


def path(file: str, folder: str = ".") -> str:
    """Path location to a file inside a folder"""
    return os.path.join(folder, file)


def bucket_names(clients) -> str:
    """Print out bucket names"""
    buckets = clients.list_buckets()["Buckets"]
    return "\n".join([bucket["Name"] for bucket in buckets])


def download_bucket(clients, bucket_name: str, folder=".") -> None:
    """Download the bucket contents"""
    bucket = clients.list_objects(Bucket=bucket_name)
    for file in bucket["Contents"]:
        if re.search(USEFUL_FILES, file["Key"]):
            clients.download_file(
                bucket_name, file["Key"], path(file["Key"], folder))


def find_file_paths(file_format: str = "", folder: str = ".") -> list[str]:
    "Return the file paths of a file format"
    return [file for file in glob.iglob(f'*.{file_format}', root_dir=folder)]


def combine_csv_files(csv_files: list, merge_file_name: str, folder: str = ".") -> None:
    """Combine multiple csv files into one csv file"""
    combined_file = pd.concat([pd.read_csv(path(file, folder)) for file in csv_files
                              if merge_file_name not in file])

    combined_file.to_csv(path(merge_file_name, folder), index=False)


def delete_files(files: list, exception: str = None, folder: str = ".") -> list[None]:
    """Delete files in folder"""
    if exception:
        files.remove(exception)
    return [os.remove(path(file, folder)) for file in files if os.path.exists(path(file, folder))]

# def combine_json_files(read_files: list, merge_file_name: str, folder: str = ".") -> None:
#     textfile_merged = open(merge_file_name, 'w')

#     for f in read_files:
#         with open(f, 'w+t') as file:
#             data = json.load(file)
#             json.dump(data, merge_file_name)

#     textfile_merged.close()


if __name__ == '__main__':
    clients = get_client(dotenv_values().get("ACCESS_KEY"),
                         dotenv_values().get("SECRET_ACCESS_KEY"))

    bucket_names(clients)
    download_bucket(clients, BUCKET_NAME, BUCKET_FOLDER)

    csv_files = find_file_paths('csv', BUCKET_FOLDER)
    combine_csv_files(csv_files, MERGE_CSV_FILE, BUCKET_FOLDER)
    delete_files(csv_files, MERGE_CSV_FILE, BUCKET_FOLDER)

    # json_files = find_files('.json', BUCKET_FOLDER)
    # combine_json_files(json_files, 'lmnh_exhibition_data.json', BUCKET_FOLDER)
    # delete_files(json_files)
