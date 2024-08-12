from ..models.departement import Department, BedDetail
from bson import ObjectId
from ..database import MongoDBManager
from typing import List, Optional
from dotenv import load_dotenv


class DepartementManagement:
    def __init__(self):
        load_dotenv()
        self.db_manager = MongoDBManager()
        self.collection = self.db_manager.get_collection("Departements")
        self.bed_collection = self.db_manager.get_collection("Beds")
        self.hospital_collection = self.db_manager.get_collection("Hospitals")

    @staticmethod
    def departement_helper(dpt_doc) -> dict:
        return ({
            "id": str(dpt_doc["_id"]),
            "hospital_id": dpt_doc['hospital_id'],
            # "departement_id": dpt_doc['departement_id'],
            "name": dpt_doc['name'],
            "location": dpt_doc['location'],
            "beds": dpt_doc['beds']
        })

    async def create_dpt(self, dpt: Department) -> dict:
        if not self.hospital_collection.find_one({"_id": ObjectId(dpt.hospital_id)}):
            raise ValueError(f"Hospital {dpt.hospital_id} does not exist")

        new_dpt = self.collection.insert_one(dpt.model_dump())
        created_dpt = self.collection.find_one({'_id': new_dpt.inserted_id})
        return self.departement_helper(created_dpt)

    async def get_dpts(self, skip: int = 0, limit: int = 10) -> List[dict]:
        dpts = []
        for dpt_doc in self.collection.find().skip(skip).limit(limit):
            dpts.append(self.departement_helper(dpt_doc))
        return dpts

    async def get_dpt(self, dpt_id: str) -> Optional[dict]:
        dpt = self.collection.find_one({'_id': ObjectId(dpt_id)})
        if dpt:
            return self.departement_helper(dpt)
        return None

    async def update_dpt(self, dpt_id: str, dpt_data: dict) -> bool:
        update_result = self.collection.update_one({'_id': ObjectId(dpt_id)}, {"$set": dpt_data})
        return update_result.modified_count > 0

    async def delete_dpt(self, dpt_id: str) -> bool:
        delete_result = self.collection.delete_one({"_id": ObjectId(dpt_id)})
        return delete_result.deleted_count > 0

    @staticmethod
    def bed_helper(bed_doc) -> dict:
        return {
            "id": str(bed_doc["_id"]),
            "hospital_id": bed_doc["hospital_id"],
            "bed_id": bed_doc["bed_id"],
            "department_id": bed_doc["department_id"],
            "status": bed_doc["status"],
        }

    # Create a new bed
    async def create_bed(self, bed: BedDetail) -> dict:
        new_bed = await self.bed_collection.insert_one(bed.model_dump())
        created_bed = await self.bed_collection.find_one({"_id": new_bed.inserted_id})
        return self.bed_helper(created_bed)

    # Retrieve all beds
    async def get_beds(self, skip: int = 0, limit: int = 10) -> List[dict]:
        beds = []
        async for bed in self.bed_collection.find().skip(skip).limit(limit):
            beds.append(self.bed_helper(bed))
        return beds

    # Retrieve a bed by ID
    async def get_bed(self, bed_id: str) -> Optional[dict]:
        bed = await self.bed_collection.find_one({"_id": ObjectId(bed_id)})
        if bed:
            return self.bed_helper(bed)
        return None

    # Update a bed
    async def update_bed(self, bed_id: str, bed_data: dict) -> bool:
        update_result = await self.bed_collection.update_one({"_id": ObjectId(bed_id)}, {"$set": bed_data})
        return update_result.modified_count > 0

    # Delete a bed
    async def delete_bed(self, bed_id: str) -> bool:
        delete_result = await self.bed_collection.delete_one({"_id": ObjectId(bed_id)})
        return delete_result.deleted_count > 0
