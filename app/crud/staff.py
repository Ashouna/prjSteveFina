from ..models.staff import Staff
from bson import ObjectId
from dotenv import load_dotenv
from ..database import MongoDBManager
from typing import List, Optional


class StaffManagement:
    def __init__(self):
        load_dotenv()
        self.db_manager = MongoDBManager()
        self.collection = self.db_manager.get_collection("Staffs")
        self.hospital_collection = self.db_manager.get_collection("Hospitals")

    @staticmethod
    def staff_heper(staff_doc) -> dict:
        return ({
            "id": str(staff_doc['_id']),
            "hospital_id": str(staff_doc['hospital_id']),
            "staff_id": staff_doc['staff_id'],
            "first_name": staff_doc['first_name'],
            "last_name": staff_doc['last_name'],
            "role": staff_doc['role'],
            "department": staff_doc['department'],
            "contact_information": staff_doc['contact_information']
        })

    async def create_staff(self, staff: Staff) -> dict:
        if not self.hospital_collection.find_one({"_id": ObjectId(staff.hospital_id)}):
            raise ValueError(f"Hospital ID: {staff.hospital_id} does not exist")

        new_staff = self.collection.insert_one(staff.model_dump())
        staff_id = new_staff.inserted_id
        self.collection.update_one({"_id": staff_id}, {"$set": {"staff_id": str(staff_id)}})
        created_staff = self.collection.find_one({"_id": new_staff.inserted_id})
        return self.staff_heper(created_staff)

    async def get_staffs(self, skip: int = 0, limit: int = 10) -> List[dict]:
        staffs = []
        for staff_doc in self.collection.find().skip(skip).limit(limit):
            staffs.append(self.staff_heper(staff_doc))
        return staffs

    async def get_staff(self, staff_id: str) -> Optional[dict]:
        staff = self.collection.find_one({"_id": ObjectId(staff_id)})
        if staff:
            return self.staff_heper(staff)
        return None

    async def update_staff(self, staff_id: str, staff_data: dict) -> bool:
        update_result = self.collection.update_one({"_id": ObjectId(staff_id)}, {"$set": staff_data})
        return update_result.modified_count > 0

    async def delete_staff(self, staff_id: str) -> bool:
        delete_staff = self.collection.delete_one({"_id": ObjectId(staff_id)})
        return delete_staff.deleted_count > 0
