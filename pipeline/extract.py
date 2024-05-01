"""Extract file"""
import os
import re
import glob
import json
from boto3 import client
from dotenv import dotenv_values
import pandas as pd

BUCKET_FOLDER = "buckets"
USEFUL_FILES = "^lmnh.*.(csv|json)$"


def path(file: str, folder: str = "./") -> str:
    """Path location to a file inside a folder"""
    return os.path.join(folder, file)


def bucket_names(clients) -> str:
    """Print out bucket names"""
    sss = clients.list_buckets()["Buckets"]
    return "\n".join([bucket["Name"] for bucket in sss])


def download_bucket(clients, bucket_name: str, folder="./") -> None:
    """Download the bucket contents"""
    bucket = clients.list_objects(Bucket=bucket_name)
    for file in bucket["Contents"]:
        if re.search(USEFUL_FILES, file["Key"]):
            clients.download_file(
                bucket_name, file["Key"], path(file["Key"], folder))


# def find_files(file_format: str = "", folder: str = "./") -> list:
#     "Return files of file format in folder"
#     bucket_files = os.listdir(folder)
#     files = [file for file in bucket_files if file.endswith(file_format)]
#     if not files:
#         raise NameError(f"No {file_format} files found")
#     return files


def find_files(file_format: str = "", folder: str = "./") -> list:
    "Return files of file format in folder"
    for file in glob.iglob(f'*.{file_format}', root_dir=folder):
        return file


def delete_files(files: list, folder: str = "./") -> None:
    """Delete files in folder"""
    for file in files:
        if os.path.exists(file):
            os.remove(path(file, folder))


def combine_csv_files(csv_files: list, merge_file_name: str, folder: str = "./") -> None:
    """Combine multiple csv files into one csv file"""
    if merge_file_name in csv_files:
        csv_files.remove(merge_file_name)
    combined_file = pd.concat(
        [pd.read_csv(path(file, folder)) for file in csv_files])
    combined_file.to_csv(path(merge_file_name, folder), index=False)


def combine_json_files(read_files: list, merge_file_name: str, folder: str = "./") -> None:
    textfile_merged = open(merge_file_name, 'w')

    for f in read_files:
        with open(f, 'w+t') as file:
            data = json.load(file)
            json.dump(data, merge_file_name)

    textfile_merged.close()


if __name__ == '__main__':
    clients = client(
        's3', aws_access_key_id=dotenv_values().get("ACCESS_KEY"),
        aws_secret_access_key=dotenv_values().get("SECRET_ACCESS_KEY"))
    folder = "./"

    # bucket_names(clients)
    # download_bucket(clients, "sigma-resources-museum", folder)

    csv_files = find_files('.csv')
    # combine_csv_files(csv_files, 'lmnh_hist_data.csv', folder)
    # delete_files(csv_files, folder)

    # json_files = find_files('.json', folder)
    # combine_json_files(json_files, 'lmnh_exhibition_data.json', folder)
    # delete_files(json_files, folder)
