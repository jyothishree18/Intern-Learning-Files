
from pathlib import Path
from urllib.parse import quote

from app.services.storage import (
    s3_client,
    presigned_s3_client,
    BUCKET_NAME,
)

from botocore.exceptions import ClientError


# ==================================
# CREATE BUCKET IF NOT EXISTS
# ==================================

def create_bucket_if_not_exists():

    if not BUCKET_NAME:
        raise RuntimeError("S3_BUCKET_NAME is not configured")

    try:
        # Check whether the bucket already exists
        s3_client.head_bucket(Bucket=BUCKET_NAME)

        print(f"Bucket '{BUCKET_NAME}' already exists")

    except ClientError as error:

        error_code = error.response.get("Error", {}).get("Code", "")
        status_code = error.response.get("ResponseMetadata", {}).get(
            "HTTPStatusCode"
        )

        # Create the bucket if it does not exist
        if error_code in ["404", "NoSuchBucket", "NotFound"] or status_code == 404:

            s3_client.create_bucket(Bucket=BUCKET_NAME)

            print(f"Bucket '{BUCKET_NAME}' created successfully")

        else:
            raise


# ==================================
# UPLOAD FILE
# ==================================

def upload_file(file_object, storage_key: str, content_type: str):

    s3_client.upload_fileobj(
        file_object,
        BUCKET_NAME,
        storage_key,
        ExtraArgs={
            "ContentType": content_type
        }
    )

    return storage_key


# ==================================
# DOWNLOAD FILE
# ==================================

def download_file(storage_key: str):

    return s3_client.get_object(
        Bucket=BUCKET_NAME,
        Key=storage_key
    )


# ==================================
# DELETE FILE
# ==================================

def delete_file(storage_key: str):

    s3_client.delete_object(
        Bucket=BUCKET_NAME,
        Key=storage_key
    )


# ==================================
# GENERATE PRESIGNED URL
# ==================================

def generate_presigned_url(storage_key: str, file_name: str = None):

    params = {
        "Bucket": BUCKET_NAME,
        "Key": storage_key,
    }

    if file_name:
        safe_name = Path(file_name).name

        params["ResponseContentDisposition"] = (
            f"attachment; filename*=UTF-8''{quote(safe_name)}"
        )

    return presigned_s3_client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=300,
    )
