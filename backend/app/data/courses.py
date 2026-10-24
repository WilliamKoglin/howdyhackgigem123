"""
Sample Texas A&M course catalog.

NOTE: This is representative demo data (CSCE-focused) so the planner works
end-to-end. Replace / extend with the official catalog as needed.
Prereqs use the "AND of OR-groups" format defined in models.Course.
"""
from app.models import Course

COURSES: dict[str, Course] = {c.code: c for c in [
    # ---- Math ----
    Course(code="MATH 151", title="Engineering Calculus I", credits=4,
           ucc_tags=["MATH"], offered=["Fall", "Spring", "Summer"]),
    Course(code="MATH 152", title="Engineering Calculus II", credits=4,
           prereqs=[["MATH 151"]], offered=["Fall", "Spring", "Summer"]),
    Course(code="MATH 251", title="Engineering Math III", credits=3,
           prereqs=[["MATH 152"]]),
    Course(code="MATH 304", title="Linear Algebra", credits=3,
           prereqs=[["MATH 152"]]),

    # ---- Computer Science core ----
    Course(code="CSCE 121", title="Intro to Program Design & Concepts", credits=4,
           offered=["Fall", "Spring", "Summer"]),
    Course(code="CSCE 221", title="Data Structures & Algorithms", credits=4,
           prereqs=[["CSCE 121"], ["MATH 151"]]),
    Course(code="CSCE 222", title="Discrete Structures for Computing", credits=3,
           prereqs=[["CSCE 121"], ["MATH 151"]]),
    Course(code="CSCE 312", title="Computer Organization", credits=4,
           prereqs=[["CSCE 221"]]),
    Course(code="CSCE 313", title="Intro to Computer Systems", credits=4,
           prereqs=[["CSCE 221"], ["CSCE 312"]]),
    Course(code="CSCE 314", title="Programming Languages", credits=3,
           prereqs=[["CSCE 221"]]),
    Course(code="CSCE 315", title="Programming Studio", credits=3,
           prereqs=[["CSCE 221"], ["CSCE 314"]]),
    Course(code="CSCE 411", title="Design & Analysis of Algorithms", credits=3,
           prereqs=[["CSCE 221"], ["CSCE 222"]]),
    Course(code="CSCE 420", title="Artificial Intelligence", credits=3,
           prereqs=[["CSCE 221"], ["CSCE 222"]]),
    Course(code="CSCE 462", title="Microcomputer Systems", credits=4,
           prereqs=[["CSCE 312"]]),
    Course(code="CSCE 482", title="Senior Capstone Design", credits=3,
           prereqs=[["CSCE 315"]]),

    # ---- Science ----
    Course(code="PHYS 206", title="Newtonian Mechanics", credits=3,
           prereqs=[["MATH 151"]], ucc_tags=["LIFE_PHYS_SCI"]),
    Course(code="PHYS 207", title="Electricity & Magnetism", credits=3,
           prereqs=[["PHYS 206"], ["MATH 152"]], ucc_tags=["LIFE_PHYS_SCI"]),
    Course(code="BIOL 111", title="Introductory Biology I", credits=4,
           ucc_tags=["LIFE_PHYS_SCI"]),

    # ---- UCC / Core electives ----
    Course(code="ENGL 103", title="Intro to Rhetoric & Composition", credits=3,
           ucc_tags=["COMMUNICATION"], offered=["Fall", "Spring", "Summer"]),
    Course(code="ENGL 210", title="Technical & Business Writing", credits=3,
           prereqs=[["ENGL 103"]], ucc_tags=["COMMUNICATION"]),
    Course(code="COMM 203", title="Public Speaking", credits=3,
           ucc_tags=["COMMUNICATION"]),
    Course(code="POLS 206", title="American National Government", credits=3,
           ucc_tags=["GOVT_POLI_SCI"]),
    Course(code="POLS 207", title="State & Local Government", credits=3,
           ucc_tags=["GOVT_POLI_SCI"]),
    Course(code="HIST 105", title="History of the US to 1877", credits=3,
           ucc_tags=["AMERICAN_HISTORY"]),
    Course(code="HIST 106", title="History of the US since 1877", credits=3,
           ucc_tags=["AMERICAN_HISTORY"]),
    Course(code="ECON 202", title="Principles of Economics", credits=3,
           ucc_tags=["SOCIAL_BEHAVIORAL"]),
    Course(code="PSYC 107", title="Intro to Psychology", credits=3,
           ucc_tags=["SOCIAL_BEHAVIORAL"]),
    Course(code="PHIL 240", title="Intro to Logic", credits=3,
           ucc_tags=["LANG_PHIL_CULTURE"]),
    Course(code="ARTS 149", title="Art History Survey", credits=3,
           ucc_tags=["CREATIVE_ARTS"]),
    Course(code="MUSC 201", title="Music Appreciation", credits=3,
           ucc_tags=["CREATIVE_ARTS"]),
]}