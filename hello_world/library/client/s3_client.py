import boto3
import os
# Create an S3 client
s3 = boto3.client('s3')


def download_file(s3_bucket, key, local_path):
    # Download the file
    try:
        file_already_exists = os.path.isfile(local_path)
        if not file_already_exists:
            s3.download_file(s3_bucket, key, local_path)
            print(f"File downloaded successfully to {local_path}")
        else:
            print(f"Skipping download of: {local_path} since it already exists")
    except Exception as e:
        print(f"Error downloading file: {e}")
