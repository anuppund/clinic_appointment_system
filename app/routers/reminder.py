from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..utils.reminder import (
    check_tomorrow_appointments
)

from ..role_checker import (
    admin_required
)

router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"]
)
@router.get("/")
def get_reminders(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    reminders = check_tomorrow_appointments(
        db
    )

    return {
        "total_reminders":
            len(reminders),

        "reminders":
            reminders
    }