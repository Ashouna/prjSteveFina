from ..models.Appointement import Appointment as model_apt
from ..crud import appointement as a
from fastapi import APIRouter, HTTPException
from typing import List

apt_router = APIRouter()
apt_crud = a.AppointmentManagement()


@apt_router.post("/", response_model=model_apt)
async def create_apt(apt: model_apt):
    try:
        return await apt_crud.create_appointment(apt)
    except Exception as e:
        raise HTTPException(404, detail=str(e))

@apt_router.get("/", response_model=List[model_apt])
async def get_apts(skip: int = 0, limit: int = 10):
    return await apt_crud.get_appointments(skip=skip, limit=limit)


@apt_router.get("/{apt_id}", response_model=model_apt)
async def get_apt(apt_id: str):
    apt = await apt_crud.get_appointment(apt_id)
    if not apt:
        raise HTTPException(404, " Aucun Rendez-vous trouver")
    return apt


@apt_router.put("/{apt_id}", response_model=model_apt)
async def update_apt(apt_id: str, apt_data: model_apt):
    update_success = await apt_crud.update_appointment(apt_id, apt_data.model_dump())
    if not update_success:
        raise HTTPException(404, "Aucun Rendez-vous trouver")
    return await apt_crud.get_appointment(apt_id)


@apt_router.delete("/{apt_id}")
async def delete_apt(apt_id: str):
    delete_success = await apt_crud.delete_appointment(apt_id)
    if not delete_success:
        raise HTTPException(404, "Aucun Rendez-vous trouver")
    return {"message": " Rendez-vous supprimer avec succes"}
