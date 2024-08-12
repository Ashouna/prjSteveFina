from pydantic import BaseModel
from typing import List, Optional


class Bed(BaseModel):
    bed_id: str
    status: str


class Department(BaseModel):
    hospital_id: Optional[str] = None
    # department_id: str
    name: str
    location: str
    beds: List[Bed]


class BedDetail(BaseModel):
    hospital_id: str
    bed_id: Optional[str] = None
    department_id: str
    status: str


class DepartmentUpdate(BaseModel):
    name: str
    location: str
    beds: List[Bed]