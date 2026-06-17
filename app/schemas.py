from pydantic import BaseModel
from datetime import date
from datetime import time
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class LoginSchema(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str
    email: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    experience: int
    consultation_fee: int
    available_days: str


class DoctorUpdate(BaseModel):
    name: str
    specialization: str
    experience: int
    consultation_fee: int
    available_days: str


class DoctorResponse(BaseModel):

    id: int
    name: str
    specialization: str
    experience: int
    consultation_fee: int
    available_days: str

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):

    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentUpdate(BaseModel):

    appointment_date: date
    appointment_time: time
    status: str


class AppointmentResponse(BaseModel):

    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str

    class Config:
        from_attributes = True

class MedicalRecordCreate(BaseModel):

    patient_id: int
    doctor_id: int
    diagnosis: str
    prescription: str
    notes: str


class MedicalRecordUpdate(BaseModel):

    diagnosis: str
    prescription: str
    notes: str


class MedicalRecordResponse(BaseModel):

    id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    prescription: str
    notes: str
    created_at: datetime

    class Config:
        from_attributes = True

