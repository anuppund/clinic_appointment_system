from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..models import Doctor
from ..schemas import (
    DoctorCreate,
    DoctorUpdate
)

from ..dependencies import get_db
from ..role_checker import admin_required

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post("/")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        experience=doctor.experience,
        consultation_fee=doctor.consultation_fee,
        available_days=doctor.available_days
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {
        "message": "Doctor Added Successfully",
        "doctor": new_doctor
    }


@router.get("/")
def get_all_doctors(
    db: Session = Depends(get_db)
):
    doctors = db.query(Doctor).all()

    return doctors


@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    updated_doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.name = updated_doctor.name
    doctor.specialization = updated_doctor.specialization
    doctor.experience = updated_doctor.experience
    doctor.consultation_fee = updated_doctor.consultation_fee
    doctor.available_days = updated_doctor.available_days

    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor Updated Successfully",
        "doctor": doctor
    }


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    db.delete(doctor)
    db.commit()

    return {
        "message": "Doctor Deleted Successfully"
    }