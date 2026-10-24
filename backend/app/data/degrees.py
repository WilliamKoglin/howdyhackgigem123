"""Sample Texas A&M degree definitions."""
from app.models import Degree, UccRequirement

# Standard TAMU University Core Curriculum (42 hours) buckets.
def _standard_ucc() -> list[UccRequirement]:
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

DEGREES: dict[str, Degree] = {d.key: d for d in [
    Degree(
        key="BS_CSCE",
        name="B.S. Computer Science",
        total_credits=120,
        required_courses=[
            "MATH 151", "MATH 152", "MATH 251", "MATH 304",
            "CSCE 121", "CSCE 221", "CSCE 222", "CSCE 312", "CSCE 313",
            "CSCE 314", "CSCE 315", "CSCE 411", "CSCE 420", "CSCE 482",
            "PHYS 206", "PHYS 207",
        ],
        ucc_requirements=_standard_ucc(),
        elective_credits=9,
    ),
    Degree(
        key="BS_CE",
        name="B.S. Computer Engineering",
        total_credits=128,
        required_courses=[
            "MATH 151", "MATH 152", "MATH 251",
            "CSCE 121", "CSCE 221", "CSCE 222", "CSCE 312", "CSCE 462",
            "PHYS 206", "PHYS 207",
        ],
        ucc_requirements=_standard_ucc(),
        elective_credits=15,
    ),
]}