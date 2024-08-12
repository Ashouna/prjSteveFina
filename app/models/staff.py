from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactInfo(BaseModel):
    phone_number: str
    email: EmailStr
    address: str


class Staff(BaseModel):
    hospital_id: Optional[str] = None
    staff_id: Optional[str] = None
    first_name: str
    last_name: str
    role: str
    department: str
    contact_information: ContactInfo


class StaffUpdate(BaseModel):
    first_name: str
    last_name: str
    role: str
    department: str
    contact_information: ContactInfo

