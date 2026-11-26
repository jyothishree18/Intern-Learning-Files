
from app.services.storage import (
    s3_client,
    presigned_s3_client,
    BUCKET_NAME,
)


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


def download_file(storage_key: str):
    return s3_client.get_object(
        Bucket=BUCKET_NAME,
        Key=storage_key
    )


def delete_file(storage_key: str):
    s3_client.delete_object(
        Bucket=BUCKET_NAME,
        Key=storage_key
    )


def generate_presigned_url(storage_key: str):
    return presigned_s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": storage_key,
        },
        ExpiresIn=300,
    )
