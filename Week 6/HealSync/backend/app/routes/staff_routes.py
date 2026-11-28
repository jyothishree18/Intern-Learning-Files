
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import staff_crud
from app.db.database import get_db
from app.core.auth import require_roles

from app.schemas.schemas import (
    StaffCreate,
    StaffResponse,
)

from app.services.staff_service import (
    create_staff_member,
    remove_staff_member,
)


router = APIRouter(
    prefix="/staff",
    tags=["Staff Management"]
)


# CREATE STAFF
@router.post(
    "",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED
)
def create_staff(
    staff_data: StaffCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    return create_staff_member(db, staff_data)


# GET ALL STAFF
@router.get(
    "",
    response_model=list[StaffResponse]
)
def list_staff(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    return staff_crud.get_staff_members(db)


# DELETE STAFF
@router.delete(
    "/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    remove_staff_member(db, staff_id)

    return None
