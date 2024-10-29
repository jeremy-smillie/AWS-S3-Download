# S3 Bucket Download Script

This script downloads all files from a specified S3 bucket to a folder on your local machine (default: `Downloads` folder). It leverages parallel downloads and multipart transfers to speed up the process, making it ideal for downloading large or numerous files.

## Prerequisites

Before running the script, ensure that you have:
1. **Python 3.8 or later** installed on macOS.
2. **AWS CLI configured** with appropriate permissions to access and download files from the S3 bucket.

## Setup Instructions for macOS

## 1. Install Python

macOS includes Python by default, but it may be outdated. To install the latest version, use [Homebrew](https://brew.sh/):

```bash
brew install python
```

## 2. Set Up a Virtual Environment
Create a virtual environment to isolate the dependencies for this script:

```bash
# Navigate to your project directory
cd path/to/your/project
```

# Create a virtual environment
```
python3 -m venv myenv
```

# Activate the virtual environment
```
source myenv/bin/activate
```

## 3. Install Required Packages
While in your virtual environment, install the necessary Python packages:

```bash
pip install boto3 botocore
```

## 4. Configure AWS CLI (if not already configured)
Ensure you have the AWS CLI configured with the credentials and permissions to access the S3 bucket. If not, run:

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, region, and default output format when prompted.
```

## 5. Update the Script
Open the script and replace '{put bucket name here}' with the name of your S3 bucket:

```python
bucket_name = '{put bucket name here}'
```
### Script Details
Key Script Components
Parallel Downloading: Utilizes ThreadPoolExecutor to download files concurrently.
Multipart Transfers: Configured to use multipart downloads for files above 5 MB, with a chunk size of 5 MB, and supports up to 20 concurrent threads for faster downloads.
Error Handling: Logs errors during the download process, enabling fault-tolerant downloading.

# Code Walkthrough
The script is structured as follows:

## Setup the S3 Client:

Initializes an S3 client with a retry configuration, allowing up to 10 retry attempts in case of transient errors.
Define the Download Directory:

Files are downloaded to the Downloads folder of the current user by default.
Transfer Configuration:

It uses a TransferConfig with multipart settings to enable parallel chunked downloads, which optimizes large file downloads.
Download Function:

Downloads each file, creating directories as needed.
It uses error handling to log any failures and continue with the next file.
Parallel Downloads Using ThreadPoolExecutor:

Lists all objects in the bucket and uses ThreadPoolExecutor to download them concurrently, up to 10 files at a time by default.
Example Usage
Run the script by executing:

```bash
python download_s3_bucket.py
```

The script will display the progress for each file it downloads and show a completion message.

# Customization

## Change Download Destination:

To download files to a different folder, change the download_folder variable:

```python
download_folder = '/path/to/your/folder'
```

## Adjust Parallel Downloads:

Modify max_workers in ThreadPoolExecutor to control the number of concurrent downloads.
Adjust Multipart Transfer Settings:

Modify multipart_threshold and multipart_chunksize in TransferConfig to set different chunk sizes or thresholds.
Troubleshooting

# Common Issues
## Permissions Error:

Please make sure your AWS CLI credentials have s3:GetObject permissions for the bucket.
Connection Errors:

If you encounter network issues, consider lowering max_workers or running the script on an EC2 instance within the same AWS region as the S3 bucket for optimal performance.

# Tips

Increasing Speed: Higher bandwidth systems can try increasing max_workers in ThreadPoolExecutor.
Running in EC2: Running this script on an EC2 instance in the same region as your S3 bucket can reduce latency and improve download speeds.

# License
This project is licensed under the MIT License.
