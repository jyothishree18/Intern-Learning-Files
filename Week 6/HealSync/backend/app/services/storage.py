
import os
import boto3

from botocore.config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MinIO connection used by the backend container
s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    region_name=os.getenv("S3_REGION", "us-east-1"),
    config=Config(signature_version="s3v4"),
)

# MinIO connection used only to generate browser-accessible URLs
presigned_s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv(
        "S3_PUBLIC_ENDPOINT_URL",
        "http://localhost:9000"
    ),
    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    region_name=os.getenv("S3_REGION", "us-east-1"),
    config=Config(signature_version="s3v4"),
)

# MinIO bucket name
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
