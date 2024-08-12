from ..models.patient import Patient as model_patient, PatientUpdate as model_update
from typing import List
from fastapi import APIRouter, HTTPException
from ..crud import patient as p


patient_router = APIRouter()
patient_crud = p.PatientManager()


@patient_router.post("/", response_model=model_patient)
async def create_patient(patient: model_patient):
    try:
        return await patient_crud.create_patient(patient)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


@patient_router.get("/", response_model=List[model_patient])
async def get_patients(skip: int = 0, limit: int = 10):
    return await patient_crud.get_patients(skip=skip, limit=limit)


@patient_router.get("/{patient_id}", response_model=model_patient)
async def get_patient(patient_id: str):
    patient = await patient_crud.get_patient(patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    return patient


# a revoir ?
@patient_router.put("/{patient_id}", response_model=model_patient)
async def update_patient(patient_id: str, patient_data: model_update):
    update_success = await patient_crud.update_patient(patient_id, patient_data.model_dump())
    if not update_success:
        raise HTTPException(404, "Patient not found")
    return await patient_crud.get_patient(patient_id)


@patient_router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    delete_success = await patient_crud.delete_patient(patient_id)
    if not delete_success:
        raise HTTPException(404, "Patient not found")
    return {"message": "Patient deleted successfully"}
