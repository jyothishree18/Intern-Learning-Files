
from sqlalchemy.orm import Session

from app.db.models import Staff


# CREATE STAFF
def create_staff(db: Session, staff_data: dict):
    staff = Staff(**staff_data)

    db.add(staff)
    db.commit()
    db.refresh(staff)

    return staff


# GET STAFF BY EMAIL
def get_staff_by_email(db: Session, email: str):
    return db.query(Staff).filter(
        Staff.email == email
    ).first()


# GET ALL STAFF
def get_staff_members(db: Session):
    return db.query(Staff).order_by(
        Staff.id.desc()
    ).all()


# GET SINGLE STAFF
def get_staff(db: Session, staff_id: int):
    return db.query(Staff).filter(
        Staff.id == staff_id
    ).first()


# DELETE STAFF
def delete_staff(db: Session, staff_id: int):
    staff = get_staff(db, staff_id)

    if staff is None:
        return False

    db.delete(staff)
    db.commit()

    return True
