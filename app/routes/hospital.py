from fastapi import APIRouter, HTTPException
from typing import List
from ..models.hospital import Hospital as model_hospital
from ..crud import hospital as h

hospital_router = APIRouter()
hospital_crud = h.HospitalManager()


@hospital_router.post("/", response_model=model_hospital)
async def create_hospital(hospital: model_hospital):
    return await hospital_crud.create_hospital(hospital)


@hospital_router.get("/", response_model=List[model_hospital])
async def read_hospitals(skip: int = 0, limit: int = 10):
    return await hospital_crud.get_hospitals(skip=skip, limit=limit)


@hospital_router.get("/{id}", response_model=model_hospital)
async def read_hospital(id: str):
    hospital = await hospital_crud.get_hospital(id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@hospital_router.patch("/{id}", response_model=model_hospital)
async def update_hospital(id: str, hospital: model_hospital):
    update_success = await hospital_crud.update_hospital(id, hospital.model_dump())
    if not update_success:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@hospital_router.delete("/{id}")
async def delete_hospital(id: str):
    delete_success = await hospital_crud.delete_hospital(id)
    if not delete_success:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"message": "Hospital deleted successfully"}
