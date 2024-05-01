import pytest
from unittest.mock import patch
from extract import bucket_names, path, download_bucket, find_files, delete_files, combine_csv_files


def test_path_valid() -> None:
    location = path("random_file", "random_folder")
    assert location == "random_folder/random_file"


@patch("extract.client")
def test_bucket_names_valid(test_client) -> None:
    test_client.list_buckets.return_value = {"Buckets": [
        {"Name": "Bucket 1"},
        {"Name": "Bucket 2"}
    ]}

    assert bucket_names(test_client) == "Bucket 1\nBucket 2"


@patch("extract.client")
def test_download_bucket_valid(test_client) -> None:
    bucket_name = "Random Bucket Name"
    test_client.list_objects.return_value = {"Contents": [
        {"Key": "lmnh.csv"},
        {"Key": "lmnh_dsf.csv"},
        {"Key": "random.csv"}
    ]}
    download_bucket(test_client, bucket_name)
    assert test_client.download_file.call_count == 2


@patch("extract.os")
def test_find_csv_files_valid(test_os) -> None:
    folder = "A random folder"
    test_os.listdir.return_value = ["file.txt",
                                    "file.csv", "random.csv", "random.txt"]

    assert find_files(folder) == ["file.csv", "random.csv"]


@patch("extract.os")
def test_find_csv_files_no_csv(test_os) -> None:
    with pytest.raises(NameError) as e_info:
        folder = "A random folder"
        test_os.listdir.return_value = ["file.txt", "random.txt"]
        find_files(folder)
        # assert e_info == "No csv files found"


@patch("extract.os")
def test_delete_files_valid(test_os) -> None:
    folder = "A random folder"
    files = ["file1", "file2"]
    test_os.remove.return_value = []
    delete_files(files, folder)
    assert test_os.remove.call_count == 2


# def combine_csv(csv_files: list, merge_file_name: str, folder: str) -> pd.DataFrame:
#     """Combine multiple csv files into one csv file"""
#     if merge_file_name in csv_files:
#         csv_files.remove(merge_file_name)
#     combined_file = pd.concat([pd.read_csv(path(file)) for file in csv_files])
#     combined_file.to_csv(path(merge_file_name, folder), index=False)

#     return combined_file

# @patch("extract.pd")
# def test_combine_csv_valid(test_pd) -> None:
#     csv_files = ["file.csv", "random.csv"]
#     merge_file_name = "merged_file"
#     folder = "a random folder"
#     test_pd.concat.return_value = pd("something")
#     test_pd.to_csv.return_value = "something"
#     combine_csv(csv_files, merge_file_name, folder)
#     assert test_pd.call_count == 5
