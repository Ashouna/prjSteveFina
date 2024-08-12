from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MedicalHistory(BaseModel):
    consultation_date: datetime
    doctor_id: str
    diagnosis: str
    treatment: str


class ContactInfo(BaseModel):
    phone_number: str
    email: str
    address: str


class Patient(BaseModel):
    hospital_id: str
    # patient_id: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: str
    medical_history: List[MedicalHistory]
    contact_information: ContactInfo


class PatientUpdate(BaseModel):
    first_name: str
    last_name: str
    medical_history: List[MedicalHistory]
    contact_information: ContactInfo
