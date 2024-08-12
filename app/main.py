# import routes
from fastapi import FastAPI
from .routes import hospital, doctor, patient, staff, departement, appointment

# import .routes.doctor as doctor
# import .routes.patient as patient
# import .routes.staff as staff
# import .routes.departement as department
# import .routes.appointment as appointment

app = FastAPI()

app.include_router(hospital.hospital_router, prefix="/hospital", tags=["hospitals"])
app.include_router(patient.patient_router, prefix="/patient", tags=["patients"])
app.include_router(doctor.doctor_router, prefix="/doctor", tags=["doctors"])
app.include_router(staff.staff_router, prefix="/staff", tags=["staff"])
app.include_router(departement.dpt_router, prefix="/departement", tags=["departments"])
app.include_router(appointment.apt_router, prefix="/appointment", tags=["appointments"])


@app.get("/")
async def root():
    return {"message": "Bienvenue dans notre gestion d'hopital "}
