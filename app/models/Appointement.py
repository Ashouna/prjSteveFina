from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional


class Appointment(BaseModel):
    hospital_id: str
    # appointment_id: Optional[str] = None
    patient_id: str
    doctor_id: str
    department_id: str
    appointment_date: datetime
    appointment_time: str
    status: str
    notes: Optional[str]
