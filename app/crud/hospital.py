from ..database import MongoDBManager
from typing import List, Optional
from ..models.hospital import Hospital  # Assurez-vous que ce modèle est correctement importé
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()


class HospitalManager:
    def __init__(self):
        self.db_manager = MongoDBManager()
        self.collection = self.db_manager.get_collection("Hospitals")

    # Convert MongoDB document to Hospital model
    @staticmethod
    def hospital_helper(hospital_doc) -> dict:
        return {
            "id": str(hospital_doc["_id"]),
            "hospital_id": str(hospital_doc["hospital_id"]),
            "name": hospital_doc["name"],
            "address": hospital_doc["address"],
            "contact_information": hospital_doc["contact_information"],
        }

    # Create a new hospital
    async def create_hospital(self, hospital: Hospital) -> dict:
        new_hospital = self.collection.insert_one(hospital.model_dump())
        # Je veux que hospital_id ait la meme valeur que _id
        hospital_id = new_hospital.inserted_id
        self.collection.update_one({"_id": hospital_id}, {"$set": {"hospital_id": hospital_id}})
        created_hospital = self.collection.find_one({"_id": new_hospital.inserted_id})
        return self.hospital_helper(created_hospital)

    # Retrieve all hospitals
    async def get_hospitals(self, skip: int = 0, limit: int = 10) -> List[dict]:
        hospitals = []
        for hospital_doc in self.collection.find().skip(skip).limit(limit):
            hospitals.append(self.hospital_helper(hospital_doc))
        return hospitals

    # Retrieve a hospital by ID
    async def get_hospital(self, id_hospital: str) -> Optional[dict]:
        hospital_doc = self.collection.find_one({"_id": ObjectId(id_hospital)})
        if hospital_doc:
            return self.hospital_helper(hospital_doc)
        return None

    # Update a hospital
    async def update_hospital(self, id_hospital: str, hospital_data: dict) -> bool:
        update_result = self.collection.update_one({"_id": ObjectId(id_hospital)}, {"$set": hospital_data})
        return update_result.modified_count > 0

    # Delete a hospital
    async def delete_hospital(self, id_hospital: str) -> bool:
        delete_result = self.collection.delete_one({"_id": ObjectId(id_hospital)})
        return delete_result.deleted_count > 0
