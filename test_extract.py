from unittest.mock import patch

from extract import bucket_names, download_bucket, find_file_paths, delete_files, combine_csv_files


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


@patch("extract.glob")
def test_find_csv_files_valid(test_glob) -> None:
    folder = "A random folder"
    test_glob.iglob.return_value = ["file.csv", "random.csv"]

    assert find_file_paths("csv", folder) == ["file.csv", "random.csv"]


@patch("extract.glob")
def test_find_csv_files_no_csv(test_glob) -> None:
    folder = "A random folder"
    test_glob.listdir.return_value = ["file.txt", "random.txt"]
    assert find_file_paths("csv", folder) == []


@patch("extract.os")
def test_delete_files_valid(test_os) -> None:
    folder = "A random folder"
    files = ["file1", "file2"]
    test_os.remove.return_value = []
    delete_files(files)
    assert test_os.remove.call_count == 2


@patch("extract.os")
def test_delete_files_valid_exception(test_os) -> None:
    folder = "A random folder"
    files = ["file1", "file2"]
    test_os.remove.return_value = []
    delete_files(files, "file1")
    assert test_os.remove.call_count == 1

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
