from fastapi import FastAPI

from .database import engine
from .models import Base

from .routers import user
from .routers import doctor

from .routers import appointment
from .routers import medical_record
from .routers import dashboard
from .routers import reminder
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(medical_record.router)
app.include_router(dashboard.router)
app.include_router(reminder.router)


@app.get("/")
def root():
    return {
        "message": "Clinic Appointment Management System Running"
    }


