from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from database import get_all_patients, get_patient

from mcp_tools import (
    tool_check_bed,
    tool_get_on_duty_nurse,
    tool_assign_bed
)

from bed_agent import run_agent


app = FastAPI()


# =========================
# Homepage
# =========================

@app.get("/")
def serve_homepage():
    return FileResponse("index.html")


# =========================
# Patients
# =========================

@app.get("/patients")
def list_patients():
    return get_all_patients()


# =========================
# Patient Triage
# =========================

@app.post("/triage/{patient_id}")
def do_triage(patient_id: int):
    patient = get_patient(patient_id)

    if not patient:
        return {"result": "Patient not found"}

    return {
        "result": "Patient details loaded successfully."
    }


# =========================
# MCP Tool Request Models
# =========================

class BedRequest(BaseModel):
    ward: str


class NurseRequest(BaseModel):
    ward: str


class AssignRequest(BaseModel):
    patient_id: int
    bed_id: int
    nurse_name: str


# =========================
# MCP Tool Routes
# =========================

@app.post("/tools/check_bed")
def check_bed(req: BedRequest):
    return tool_check_bed(req.ward)


@app.post("/tools/get_on_duty_nurse")
def get_on_duty_nurse(req: NurseRequest):
    return tool_get_on_duty_nurse(req.ward)


@app.post("/tools/assign_bed")
def assign_bed(req: AssignRequest):
    return tool_assign_bed(
        req.patient_id,
        req.bed_id,
        req.nurse_name
    )


# =========================
# AI Agent Route
# =========================

class AgentRequest(BaseModel):
    patient_id: int
    ward: str


@app.post("/agent/assign_bed")
def agent_assign_bed(req: AgentRequest):
    result = run_agent(req.patient_id, req.ward)

    return {
        "result": result
    }