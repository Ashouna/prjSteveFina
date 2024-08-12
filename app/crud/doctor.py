from ..models.doctor import Doctor
from ..database import MongoDBManager
from typing import List, Optional
from dotenv import load_dotenv
from bson import ObjectId


class DoctorManager:
    def __init__(self):
        load_dotenv()
        self.db_manager = MongoDBManager()
        self.collection = self.db_manager.get_collection("Doctors")
        self.hospital_collection = self.db_manager.get_collection("Hospitals")

    @staticmethod
    def doctor_helper(doctor_doc) -> dict:
        return ({
            "id": str(doctor_doc["_id"]),
            # "doctor_id": str(doctor_doc["_id"]),
            "hospital_id": doctor_doc["hospital_id"],
            "first_name": doctor_doc["first_name"],
            "last_name": doctor_doc["last_name"],
            "specialty": doctor_doc["specialty"],
            "availability": doctor_doc["availability"],
            "contact_information": doctor_doc["contact_information"]
        })

    async def create_doctor(self, doctor: Doctor) -> dict:
        if not self.hospital_collection.find_one({"_id": ObjectId(doctor.hospital_id)}):
            raise ValueError(f"Hospital ID: {doctor.hospital_id} does not exist")

        new_doctor = self.collection.insert_one(doctor.model_dump())
        created_doctor = self.collection.find_one({'_id': new_doctor.inserted_id})
        return self.doctor_helper(created_doctor)

    async def get_doctors(self, skip: int = 0, limit: int = 10) -> List[dict]:
        doctors = []
        for doctor_doc in self.collection.find().skip(skip).limit(limit):
            doctors.append(self.doctor_helper(doctor_doc))
        return doctors

    async def get_doctor(self, id_doctor: str) -> Optional[dict]:
        doctor_doc = self.collection.find_one({'_id': ObjectId(id_doctor)})
        if doctor_doc:
            return self.doctor_helper(doctor_doc)
        return None

    async def update_doctor(self, id_doctor: str, doctor_data: dict) -> bool:
        update_result = self.collection.update_one({'_id': ObjectId(id_doctor)}, {'$set': doctor_data})
        return update_result.modified_count > 0

    async def delete_doctor(self, id_doctor: str) -> bool:
        delete_result = self.collection.delete_one({'_id': ObjectId(id_doctor)})
        return delete_result.deleted_count > 0
