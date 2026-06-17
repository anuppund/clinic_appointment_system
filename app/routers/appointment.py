from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..models import (
    Appointment,
    User,
    Doctor
)

from ..schemas import (
    AppointmentCreate,
    AppointmentUpdate
)

from ..dependencies import get_db
from ..security import get_current_user
from ..role_checker import patient_required
from ..role_checker import doctor_required
from ..permissions import verify_patient_access

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("/")
def book_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(patient_required)
):

    verify_patient_access(
        current_user,
        appointment.patient_id
    )

    patient = db.query(User).filter(
        User.id == appointment.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    existing_appointment = db.query(
        Appointment
    ).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date == appointment.appointment_date,
        Appointment.appointment_time == appointment.appointment_time,
        Appointment.status == "Booked"
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="Doctor already booked at this time"
        )

    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "message": "Appointment Booked Successfully",
        "appointment": new_appointment
    }


@router.get("/")
def get_all_appointments(
    db: Session = Depends(get_db)
):
    return db.query(
        Appointment
    ).all()


@router.get("/my")
def my_appointments(
    db: Session = Depends(get_db),
    current_user=Depends(patient_required)
):

    appointments = db.query(
        Appointment
    ).filter(
        Appointment.patient_id == current_user["id"]
    ).all()

    return appointments


@router.get("/doctor/all")
def doctor_view_appointments(
    db: Session = Depends(get_db),
    current_user=Depends(doctor_required)
):

    appointments = db.query(
        Appointment
    ).all()

    return appointments


@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


@router.put("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    updated_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.appointment_date = updated_data.appointment_date
    appointment.appointment_time = updated_data.appointment_time
    appointment.status = updated_data.status

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment Updated",
        "appointment": appointment
    }


@router.delete("/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = "Cancelled"

    db.commit()

    return {
        "message": "Appointment Cancelled"
    }