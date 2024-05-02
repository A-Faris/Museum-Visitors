from boto3 import client
from dotenv import dotenv_values
if __name__ == '__main__':
    config = dotenv_values()
    s3 = client('s3',
                aws_access_key_id=config.get("ACCESS_KEY"),
                aws_secret_access_key=config.get("SECRET_ACCESS_KEY")
                )
    bucket = s3.list_objects(Bucket="sigma-resources-museum")
    for file in bucket["Contents"]:
        s3.download_file("sigma-resources-museum",
                         file["Key"], f"./data/{file["Key"]}")
