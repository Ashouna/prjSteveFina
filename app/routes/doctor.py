from ..models.doctor import Doctor as model_doctor, DoctorUpdate
from fastapi import APIRouter, HTTPException
from typing import List
from ..crud import doctor as d

doctor_router = APIRouter()
doctor_crud = d.DoctorManager()


@doctor_router.post("/", response_model=model_doctor)
async def create_doctor(doctor: model_doctor):
    return await doctor_crud.create_doctor(doctor)


@doctor_router.get("/", response_model=List[model_doctor])
async def get_doctors(skip: int = 0, limit: int = 10):
    return await doctor_crud.get_doctors(skip=skip, limit=limit)


@doctor_router.get("/{doctor_id}", response_model=model_doctor)
async def get_doctor(doctor_id: str):
    doctor = await doctor_crud.get_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")
    return doctor


@doctor_router.put("/{doctor_id}", response_model=model_doctor)
async def update_doctor(doctor_id: str, doctor_data: DoctorUpdate):
    update_success = await doctor_crud.update_doctor(doctor_id, doctor_data.model_dump())
    if not update_success:
        raise HTTPException(404, "Doctor not found")
    return await doctor_crud.get_doctor(doctor_id)


@doctor_router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: str):
    delete_success = await doctor_crud.delete_doctor(doctor_id)
    if not delete_success:
        raise HTTPException(404, "Doctor not found")
    return {"message": "Doctor deleted successfully"}
