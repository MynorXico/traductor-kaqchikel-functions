import boto3

# Create an S3 client
s3 = boto3.client('s3')


def download_file(s3_bucket, key, local_path):
    # Download the file
    try:
        s3.download_file(s3_bucket, key, local_path)
        print(f"File downloaded successfully to {local_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")
