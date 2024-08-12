from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Availability(BaseModel):
    day: str
    start_time: str
    end_time: str


class ContactInfo(BaseModel):
    phone_number: str
    email: EmailStr
    office_address: str


class Doctor(BaseModel):
    hospital_id: str
    # doctor_id: Optional[str] = None
    first_name: str
    last_name: str
    specialty: str
    availability: List[Availability]
    contact_information: ContactInfo


class DoctorUpdate(BaseModel):
    first_name: str
    last_name: str
    availability: List[Availability]
    contact_information: ContactInfo
