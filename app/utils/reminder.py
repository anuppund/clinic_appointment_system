from datetime import date
from datetime import timedelta

from sqlalchemy.orm import Session

from ..models import (
    Appointment,
    User,
    Doctor
)


def check_tomorrow_appointments(
    db: Session
):

    tomorrow = date.today() + timedelta(days=1)

    appointments = db.query(
        Appointment
    ).filter(
        Appointment.appointment_date == tomorrow,
        Appointment.status == "Booked"
    ).all()

    reminders = []

    for appointment in appointments:

        patient = db.query(User).filter(
            User.id == appointment.patient_id
        ).first()

        doctor = db.query(Doctor).filter(
            Doctor.id == appointment.doctor_id
        ).first()

        reminder_message = (
            f"Reminder: "
            f"{patient.name} has an appointment "
            f"with {doctor.name} on "
            f"{appointment.appointment_date} "
            f"at {appointment.appointment_time}"
        )

        reminders.append(
            reminder_message
        )

    return reminders