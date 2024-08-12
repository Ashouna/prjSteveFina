from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactInfo(BaseModel):
    phone_number: Optional[str]
    email: Optional[EmailStr]


class Hospital(BaseModel):
    hospital_id: Optional[str] = None  # `hospital_id` peut être None initialement
    name: str
    address: str
    contact_information: Optional[ContactInfo]
