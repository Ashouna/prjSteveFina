# from typing import List, Optional
# from ..models import hospital as model_hospital
# from ..crud import hospital as crud_hospital
#
#
# def __init__(self):
#     self.crud = crud_hospital.HospitalManager()
#
#
# async def create_hospital(self, hospital: model_hospital) -> dict:
#     return await self.crud.create_hospital(hospital)
#
#
# async def get_hospitals(self, skip: int = 0, limit: int = 10) -> List[dict]:
#     return await self.crud.get_hospitals(skip=skip, limit=limit)
#
#
# async def get_hospital(self, id: str) -> Optional[dict]:
#     return await self.crud.get_hospital(id)
#
#
# async def update_hospital(self, id: str, hospital_data: dict) -> bool:
#     return await self.crud.update_hospital(id, hospital_data)
#
#
# async def delete_hospital(self, id: str) -> bool:
#     return await self.crud.delete_hospital(id)
