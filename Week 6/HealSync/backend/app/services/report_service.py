
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import report_crud
from app.services.storage_service import (
    upload_file,
    download_file,
    delete_file,
    generate_presigned_url,
)


def create_report_record(
    db: Session,
    report_data: dict,
    file,
    storage_key: str,
    content_type: str
):
    try:
        # Upload file to MinIO
        upload_file(
            file,
            storage_key,
            content_type
        )

        # Save report details in PostgreSQL
        return report_crud.create_report(
            db,
            report_data
        )

    except IntegrityError:
        db.rollback()
        remove_storage_file(storage_key)
        raise

    except Exception as exc:
        db.rollback()
        remove_storage_file(storage_key)

        print("Report upload error:", repr(exc))
        raise


def get_report_file(storage_key: str):
    return download_file(storage_key)


def get_report_presigned_url(storage_key: str, file_name: str = None):
    return generate_presigned_url(storage_key, file_name)


def delete_report_record(db: Session, report):
    # Delete file from MinIO
    delete_file(report.storage_key)

    # Delete report record from PostgreSQL
    report_crud.delete_report(db, report)


def remove_storage_file(storage_key: str):
    try:
        delete_file(storage_key)
    except Exception as exc:
        print("Storage cleanup failed:", repr(exc))
