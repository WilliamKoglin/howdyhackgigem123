"""FastAPI entrypoint."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import PlanRequest, PlanResponse
from app.planner import build_plan
from app.data.degrees import DEGREES
from app.data.courses import COURSES

app = FastAPI(title="TAMU Degree Planner API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/degrees")
def list_degrees():
    """List selectable degrees (for the dropdown)."""
    return [
        {"key": d.key, "name": d.name, "total_credits": d.total_credits}
        for d in DEGREES.values()
    ]


@app.get("/degrees/{degree_key}")
def get_degree(degree_key: str):
    """Full degree detail: required courses + UCC buckets."""
    degree = DEGREES.get(degree_key)
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")
    return degree


@app.get("/courses")
def list_courses():
    """Full catalog — used by the frontend to let users mark completed work."""
    return list(COURSES.values())


@app.post("/plan", response_model=PlanResponse)
def create_plan(req: PlanRequest):
    """Generate the recommended semester-by-semester plan."""
    try:
        return build_plan(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))