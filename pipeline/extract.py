"""Extract file"""
from multiprocessing import Value
import os
import re
from boto3 import client, resource
from dotenv import dotenv_values
import pandas as pd


ACCESS_KEY = dotenv_values().get("ACCESS_KEY")
SECRET_ACCESS_KEY = dotenv_values().get("SECRET_ACCESS_KEY")
BUCKET_FOLDER = "buckets"
USEFUL_FILES = "^lmnh.*.(csv|json)$"


def path(file, folder=BUCKET_FOLDER) -> str:
    """Path location to a file inside a folder"""
    return os.path.join(folder, file)


def download_bucket(bucket_name) -> None:
    """Download the bucket contents"""
    sss = client(
        's3', aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_ACCESS_KEY)

    bucket = sss.list_objects(Bucket=bucket_name)

    for file in bucket["Contents"]:
        if re.search(USEFUL_FILES, file["Key"]):
            sss.download_file(bucket_name, file["Key"], path(file["Key"]))


def find_csv_files(folder) -> list:
    "Return csv files"
    bucket_files = os.listdir(folder)
    csv_files = [file for file in bucket_files if file.endswith('.csv')]
    if not csv_files:
        raise ValueError("No csv files found")
    return csv_files


def delete_csv(csv_files, folder) -> None:
    """Delete csv files"""
    for file in csv_files:
        os.remove(path(file, folder))


def combine_csv(csv_files, file_name, folder) -> pd.DataFrame:
    """Combine multiple csv files into one csv file"""
    combined_file = pd.concat([pd.read_csv(path(file)) for file in csv_files])
    combined_file.to_csv(path(file_name, folder), index=False)

    return combined_file


def bucket_names() -> str:
    """Print out bucket names"""
    sss = resource(
        's3', aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_ACCESS_KEY)

    return "\n".join([bucket.name for bucket in sss.buckets.all()])


if __name__ == '__main__':
    print(bucket_names())
    download_bucket("sigma-resources-museum")
    csv_files = find_csv_files(BUCKET_FOLDER)
    combine_csv(csv_files, 'lmnh_hist_data.csv', BUCKET_FOLDER)
    delete_csv(csv_files, BUCKET_FOLDER)
