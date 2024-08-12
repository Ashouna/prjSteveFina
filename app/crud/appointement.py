from ..models.Appointement import Appointment
from bson import ObjectId
from dotenv import load_dotenv
from ..database import MongoDBManager
from typing import List, Optional


class AppointmentManagement:
    def __init__(self):
        load_dotenv()
        self.db_manager = MongoDBManager()
        self.collection = self.db_manager.get_collection("Appointements")
        self.hospital = self.db_manager.get_collection("Hospitals")
        self.patient = self.db_manager.get_collection("Patients")
        self.department = self.db_manager.get_collection("Departments")
        self.doctor = self.db_manager.get_collection("Doctors")

    @staticmethod
    def appointment_helper(appointment_doc) -> dict:
        return {
            "id": str(appointment_doc["_id"]),
            "hospital_id": appointment_doc["hospital_id"],
            "patient_id": appointment_doc["patient_id"],
            "doctor_id": appointment_doc["doctor_id"],
            "department_id": appointment_doc["department_id"],
            "appointment_date": appointment_doc["appointment_date"],
            "appointment_time": appointment_doc["appointment_time"],
            "status": appointment_doc["status"],
            "notes": appointment_doc.get("notes"),
        }

    async def create_appointment(self, appointment: Appointment) -> dict:

        new_appointment = await self.collection.insert_one(appointment.model_dump())
        created_appointment = await self.collection.find_one({"_id": new_appointment.inserted_id})
        return self.appointment_helper(created_appointment)

    async def get_appointments(self, skip: int = 0, limit: int = 10) -> List[dict]:
        appointments = []
        for appointment in self.collection.find().skip(skip).limit(limit):
            appointments.append(self.appointment_helper(appointment))
        return appointments

    async def get_appointment(self, id: str) -> Optional[dict]:
        appointment = self.collection.find_one({"_id": ObjectId(id)})
        if appointment:
            return self.appointment_helper(appointment)
        return None

    async def update_appointment(self, id: str, appointment_data: dict) -> bool:
        update_result = self.collection.update_one({"_id": ObjectId(id)}, {"$set": appointment_data})
        return update_result.modified_count > 0

    async def delete_appointment(self, id: str) -> bool:
        delete_result = self.collection.delete_one({"_id": ObjectId(id)})
        return delete_result.deleted_count > 0
