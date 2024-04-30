"""Extract file"""
import os
import re
from boto3 import client
from dotenv import dotenv_values
import pandas as pd

BUCKET_FOLDER = "buckets"
USEFUL_FILES = "^lmnh.*.(csv|json)$"


def path(file: str, folder: str = BUCKET_FOLDER) -> str:
    """Path location to a file inside a folder"""
    return os.path.join(folder, file)


def bucket_names(clients) -> str:
    """Print out bucket names"""
    sss = clients.list_buckets()["Buckets"]
    return "\n".join([bucket["Name"] for bucket in sss])


def download_bucket(clients, bucket_name: str) -> None:
    """Download the bucket contents"""
    bucket = clients.list_objects(Bucket=bucket_name)
    for file in bucket["Contents"]:
        if re.search(USEFUL_FILES, file["Key"]):
            clients.download_file(bucket_name, file["Key"], path(file["Key"]))


def find_csv_files(folder: str) -> list:
    "Return csv files"
    bucket_files = os.listdir(folder)
    csv_files = [file for file in bucket_files if file.endswith('.csv')]
    if not csv_files:
        raise NameError("No csv files found")
    return csv_files


def delete_files(files: list, folder: str) -> None:
    """Delete csv files"""
    for file in files:
        os.remove(path(file, folder))


def combine_csv(csv_files: list, merge_file_name: str, folder: str) -> pd.DataFrame:
    """Combine multiple csv files into one csv file"""
    if merge_file_name in csv_files:
        csv_files.remove(merge_file_name)
    combined_file = pd.concat([pd.read_csv(path(file)) for file in csv_files])
    combined_file.to_csv(path(merge_file_name, folder), index=False)

    return combined_file


if __name__ == '__main__':
    clients = client(
        's3', aws_access_key_id=dotenv_values().get("ACCESS_KEY"),
        aws_secret_access_key=dotenv_values().get("SECRET_ACCESS_KEY"))
    print(bucket_names(clients))
    download_bucket(clients, "sigma-resources-museum")
    csv_files = find_csv_files(BUCKET_FOLDER)
    combine_csv(csv_files, 'lmnh_hist_data.csv', BUCKET_FOLDER)
    delete_files(csv_files, BUCKET_FOLDER)
