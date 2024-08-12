from ..models.staff import Staff as model_staff, StaffUpdate as model_staffUpdate
from fastapi import APIRouter, HTTPException
from typing import List
from ..crud import staff as s

staff_router = APIRouter()
staff_crud = s.StaffManagement()


@staff_router.post("/", response_model=model_staff)
async def create_staff(staff: model_staff):
    try:
        return await staff_crud.create_staff(staff)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@staff_router.get("/", response_model=List[model_staff])
async def get_staffs(skip: int = 0, limit: int = 10):
    return await staff_crud.get_staffs(skip=skip, limit=limit)


@staff_router.get("/{staff_id}", response_model=model_staff)
async def get_staff(staff_id: str):
    staff = await staff_crud.get_staff(staff_id)
    if not staff:
        raise HTTPException(404, "Staff not found")
    return staff


@staff_router.put("/{staff_id}", response_model=model_staff)
async def update_staff(staff_id: str, staff_data: model_staffUpdate):
    update_success = await staff_crud.update_staff(staff_id, staff_data.model_dump())
    if not update_success:
        raise HTTPException(404, "Staff not found")
    return await staff_crud.get_staff(staff_id)


@staff_router.delete("/{staff_id}")
async def delete_staff(staff_id: str):
    delete_success = await staff_crud.delete_staff(staff_id)
    if not delete_success:
        raise HTTPException(404, "Staff not found")
    return {"message": "Staff deleted successfully"}
