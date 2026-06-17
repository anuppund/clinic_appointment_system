from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(
        String,
        unique=True,
        index=True
    )

    password = Column(String)

    role = Column(String)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    specialization = Column(
        String,
        nullable=False
    )

    experience = Column(
        Integer
    )

    consultation_fee = Column(
        Integer
    )

    available_days = Column(
        String
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    appointment_date = Column(
        Date
    )

    appointment_time = Column(
        Time
    )

    status = Column(
        String,
        default="Booked"
    )


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    diagnosis = Column(
        String,
        nullable=False
    )

    prescription = Column(
        String,
        nullable=False
    )

    notes = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )