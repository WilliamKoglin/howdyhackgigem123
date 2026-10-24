"""
Loads the course + degree catalog from JSON files into Pydantic models.

Edit the data in app/data/catalog/*.json — this module just parses it.
"""
from __future__ import annotations
import json
from pathlib import Path

from app.models import Course, Degree, UccRequirement

CATALOG_DIR = Path(__file__).parent / "catalog"
COURSES_FILE = CATALOG_DIR / "courses.json"
DEGREES_FILE = CATALOG_DIR / "degrees.json"


def _standard_ucc() -> list[UccRequirement]:
    """The standard TAMU University Core Curriculum (42 hours)."""
    return [
        UccRequirement(key="COMMUNICATION", name="Communication", credits_required=6),
        UccRequirement(key="MATH", name="Mathematics", credits_required=3),
        UccRequirement(key="LIFE_PHYS_SCI", name="Life & Physical Sciences", credits_required=6),
        UccRequirement(key="LANG_PHIL_CULTURE", name="Language, Philosophy & Culture", credits_required=3),
        UccRequirement(key="CREATIVE_ARTS", name="Creative Arts", credits_required=3),
        UccRequirement(key="AMERICAN_HISTORY", name="American History", credits_required=6),
        UccRequirement(key="GOVT_POLI_SCI", name="Government/Political Science", credits_required=6),
        UccRequirement(key="SOCIAL_BEHAVIORAL", name="Social & Behavioral Sciences", credits_required=3),
    ]


def _read_json(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Catalog file missing: {path}")
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(f"{path.name} must contain a JSON array at the top level.")
    return data


def load_courses() -> dict[str, Course]:
    courses: dict[str, Course] = {}
    for i, raw in enumerate(_read_json(COURSES_FILE)):
        try:
            course = Course(**raw)
        except Exception as exc:  # pydantic ValidationError, etc.
            raise ValueError(f"courses.json entry #{i} is invalid: {exc}") from exc
        if course.code in courses:
            raise ValueError(f"Duplicate course code in courses.json: {course.code}")
        courses[course.code] = course
    return courses


def load_degrees() -> dict[str, Degree]:
    degrees: dict[str, Degree] = {}
    for i, raw in enumerate(_read_json(DEGREES_FILE)):
        raw = dict(raw)  # don't mutate the parsed JSON in place

        # Expand the "STANDARD" shorthand into the standard core.
        ucc = raw.get("ucc_requirements")
        if ucc == "STANDARD":
            raw["ucc_requirements"] = _standard_ucc()

        try:
            degree = Degree(**raw)
        except Exception as exc:
            raise ValueError(f"degrees.json entry #{i} is invalid: {exc}") from exc
        if degree.key in degrees:
            raise ValueError(f"Duplicate degree key in degrees.json: {degree.key}")
        degrees[degree.key] = degree
    return degrees