from ..models.departement import Department as model_dpt, BedDetail as model_bed, DepartmentUpdate
from fastapi import APIRouter, HTTPException
from typing import List
from ..crud import departement as d

dpt_router = APIRouter()
dpt_crud = d.DepartementManagement()


@dpt_router.post("/", response_model=model_dpt)
async def create_dpt(dpt: model_dpt):
    try:
        return await dpt_crud.create_dpt(dpt)
    except ValueError as e:
        raise HTTPException(404, detail=str(e))


@dpt_router.get("/", response_model=List[model_dpt])
async def get_dpts(skip: int = 0, limit: int = 10):
    return await dpt_crud.get_dpts(skip=skip, limit=limit)


@dpt_router.get("/{dpt_id}", response_model=model_dpt)
async def get_dpt(dpt_id: str):
    dpt = await dpt_crud.get_dpt(dpt_id)
    if not dpt:
        raise HTTPException(404, "Aucun département trouver")
    return dpt


@dpt_router.put("/{dpt_id}", response_model=model_dpt)
async def update_dpt(dpt_id: str, dpt_data: DepartmentUpdate):
    update_success = await dpt_crud.update_dpt(dpt_id, dpt_data.model_dump())
    if not update_success:
        raise HTTPException(404, "Aucun département trouver")
    return await dpt_crud.get_dpt(dpt_id)


@dpt_router.delete("/{dpt_id}")
async def delete_dpt(dpt_id: str):
    delete_success = await dpt_crud.delete_dpt(dpt_id)
    if not delete_success:
        raise HTTPException(404, "Aucun département trouver")
    return {"message": "Departement supprimer avec succes"}


@dpt_router.post("/beds", response_model=model_bed)
async def create_bed(bed: model_bed):
    return await dpt_crud.create_bed(bed)


@dpt_router.get("/beds", response_model=List[model_bed])
async def get_beds(skip=0, limit=10):
    return await dpt_crud.get_beds(skip=skip, limit=limit)


@dpt_router.get("beds/{bed_id}", response_model=model_bed)
async def get_bed(bed_id: str):
    bed = await dpt_crud.get_bed(bed_id)
    if not bed:
        raise HTTPException(404, "Aucun Lit trouvé")
    return bed


@dpt_router.put("beds/{bed_id}", response_model=model_bed)
async def update_bed(bed_id: str, bed: model_bed):
    update_success = await dpt_crud.update_bed(bed_id, bed.model_dump())
    if not update_success:
        raise HTTPException(404, "Aucun Lit trouvé")
    return update_success


@dpt_router.delete("/beds/{bed_id}")
async def delete_bed(bed_id: str):
    delete_success = await dpt_crud.delete_bed(bed_id)
    if not delete_success:
        raise HTTPException(404, "Aucun Lit trouvé")
    return {"message": "Lit supprimé"}
