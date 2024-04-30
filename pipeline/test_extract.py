from unittest.mock import patch
from extract import bucket_names, path, download_bucket, find_csv_files, delete_files, combine_csv


def test_path_valid():
    location = path("random_file", "random_folder")
    assert location == "random_folder/random_file"


# @patch("extract.client")
# def test_bucket_names_valid(test_client):
#     test_client.list_buckets.return_value = {"Buckets": [{
#         "Name":
#     }

#     ]}


# def bucket_names(clients) -> str:
#     """Print out bucket names"""
#     sss = clients.list_buckets()["Buckets"]
#     return "\n".join([bucket["Name"] for bucket in sss])
