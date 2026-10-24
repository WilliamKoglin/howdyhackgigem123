"""Pydantic schemas shared across API + planner."""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

# ---------- Catalog data shapes ----------

class Course(BaseModel):
    code: str                       # e.g. "CSCE 121"
    title: str
    credits: int
    # Prerequisites expressed in CNF-ish form: a list of "OR groups".
    # ALL groups must be satisfied; within a group ANY one course satisfies it.
    # [["MATH 151"], ["CSCE 110", "CSCE 111"]] => MATH 151 AND (CSCE 110 OR CSCE 111)
    prereqs: list[list[str]] = Field(default_factory=list)
    # UCC / core categories this course can satisfy (e.g. "LANG_PHIL_CULTURE")
    ucc_tags: list[str] = Field(default_factory=list)
    # Terms the course is typically offered.
    offered: list[Literal["Fall", "Spring", "Summer"]] = Field(
        default_factory=lambda: ["Fall", "Spring"]
    )

class UccRequirement(BaseModel):
    """A University Core Curriculum bucket that needs N credits."""
    key: str
    name: str
    credits_required: int

class Degree(BaseModel):
    key: str
    name: str
    total_credits: int
    required_courses: list[str]           # explicit course codes
    ucc_requirements: list[UccRequirement]
    # Free elective credits beyond named courses + UCC
    elective_credits: int = 0

# ---------- Request / response shapes ----------

class CompletedCourse(BaseModel):
    code: str
    # "PRE_COLLEGE" for AP/dual credit/transfer, else "Fall 2024" etc.
    term: str = "PRE_COLLEGE"

class PlanRequest(BaseModel):
    degree_key: str
    completed: list[CompletedCourse] = Field(default_factory=list)
    start_term: str = "Fall"              # season the NEXT planned term begins
    start_year: int = 2025
    max_credits_per_term: int = 15
    include_summer: bool = False

class PlannedCourse(BaseModel):
    code: str
    title: str
    credits: int
    reason: str                            # why it's scheduled here

class PlannedTerm(BaseModel):
    term: str                              # "Fall 2025"
    courses: list[PlannedCourse]
    credits: int

class PlanResponse(BaseModel):
    degree: str
    terms: list[PlannedTerm]
    total_terms: int
    completed_credits: int
    remaining_credits: int
    warnings: list[str] = Field(default_factory=list)