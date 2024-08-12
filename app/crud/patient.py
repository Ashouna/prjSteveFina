from ..models.patient import Patient
from dotenv import load_dotenv
from ..database import MongoDBManager
from bson import ObjectId
from typing import List, Optional


class PatientManager:
    def __init__(self):
        load_dotenv()
        self.db_manager = MongoDBManager()
        self.collection = self.db_manager.get_collection("Patients")
        self.hospital_collection = self.db_manager.get_collection("Hospitals")

    @staticmethod
    def patient_helper(patient_doc) -> dict:
        return ({
            "id": str(patient_doc["_id"]),
            # "patient_id": patient_doc["patient_id"],
            "hospital_id": str(patient_doc["hospital_id"]),
            "first_name": patient_doc['first_name'],
            'last_name': patient_doc['last_name'],
            "date_of_birth": patient_doc['date_of_birth'],
            "gender": patient_doc['gender'],
            "contact_information": patient_doc['contact_information'],
            "medical_history": patient_doc["medical_history"]
        })

    async def create_patient(self, patient: Patient) -> dict:
        if not self.hospital_collection.find_one({"_id": ObjectId(patient.hospital_id)}):
            raise ValueError(f"Hospital ID {patient.hospital_id} does not exist")

        new_patient = self.collection.insert_one(patient.model_dump())
        created_patient = self.collection.find_one({'_id': new_patient.inserted_id})
        return self.patient_helper(created_patient)

    async def get_patients(self, skip: int = 0, limit: int = 10) -> List[dict]:
        patients = []
        for patient_doc in self.collection.find().skip(skip).limit(limit):
            patients.append(self.patient_helper(patient_doc))
        return patients

    async def get_patient(self, id_patient: str) -> Optional[dict]:
        patient_doc = self.collection.find_one({'_id': ObjectId(id_patient)})
        if patient_doc:
            return self.patient_helper(patient_doc)
        return None

    async def update_patient(self, id_patient: str, patient_data: dict) -> bool:
        update_result = self.collection.update_one({'_id': ObjectId(id_patient)}, {"$set": patient_data})
        return update_result.modified_count > 0

    async def delete_patient(self, id_patient: str) -> bool:
        delete_result = self.collection.delete_one({'_id': ObjectId(id_patient)})
        return delete_result.deleted_count > 0
