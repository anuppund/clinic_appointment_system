from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..models import (
    MedicalRecord,
    User,
    Doctor
)

from ..schemas import (
    MedicalRecordCreate,
    MedicalRecordUpdate
)

from ..dependencies import get_db
from ..security import get_current_user
from ..role_checker import doctor_required
from ..role_checker import patient_required
from ..permissions import verify_patient_access

router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"]
)


@router.post("/")
def create_medical_record(
    record: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(doctor_required)
):
    patient = db.query(User).filter(
        User.id == record.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == record.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    new_record = MedicalRecord(
        patient_id=record.patient_id,
        doctor_id=record.doctor_id,
        diagnosis=record.diagnosis,
        prescription=record.prescription,
        notes=record.notes
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "Medical Record Created",
        "record": new_record
    }


@router.get("/")
def get_all_records(
    db: Session = Depends(get_db)
):
    return db.query(
        MedicalRecord
    ).all()


@router.get("/my")
def my_medical_records(
    db: Session = Depends(get_db),
    current_user=Depends(patient_required)
):

    records = db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.patient_id == current_user["id"]
    ).all()

    return records


@router.get("/patient/{patient_id}")
def get_patient_records(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    verify_patient_access(
        current_user,
        patient_id
    )

    return db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.patient_id == patient_id
    ).all()


@router.get("/{record_id}")
def get_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return record


@router.put("/{record_id}")
def update_record(
    record_id: int,
    updated_record: MedicalRecordUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(doctor_required)
):
    record = db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    record.diagnosis = updated_record.diagnosis
    record.prescription = updated_record.prescription
    record.notes = updated_record.notes

    db.commit()
    db.refresh(record)

    return {
        "message": "Record Updated",
        "record": record
    }


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(doctor_required)
):
    record = db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Record Deleted"
    }