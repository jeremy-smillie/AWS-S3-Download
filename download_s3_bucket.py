import boto3
import os
import concurrent.futures
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from boto3.s3.transfer import TransferConfig

# Initialize the S3 client with retry configuration
s3 = boto3.client('s3', config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))

# Specify the S3 bucket name
bucket_name = '{put bucket name here}'

# Set the download destination folder (Downloads folder in this case)
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

# Configure TransferConfig for faster downloads
transfer_config = TransferConfig(
    multipart_threshold=5 * 1024 * 1024,  # 5 MB threshold for multipart
    max_concurrency=20,                   # Number of concurrent threads
    multipart_chunksize=5 * 1024 * 1024,  # Set chunk size to 5 MB
    use_threads=True
)

# Function to download a single file with error handling
def download_file(key):
    file_path = os.path.join(download_folder, key)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    print(f"Downloading {key} to {file_path}")
    try:
        s3.download_file(bucket_name, key, file_path, Config=transfer_config)
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to download {key}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading {key}: {e}")

# Main function to list objects and download them in parallel
def download_s3_bucket():
    paginator = s3.get_paginator('list_objects_v2')
    keys = [obj['Key'] for page in paginator.paginate(Bucket=bucket_name) for obj in page.get('Contents', [])]

    # Download files in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_file, keys)

# Run the download function
download_s3_bucket()
print("Download completed.")

