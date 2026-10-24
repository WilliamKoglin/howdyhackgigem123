"""
Degree planning engine.

Algorithm (greedy topological scheduling):
  1. Compute the full set of courses still needed:
       - explicit required_courses not yet completed
       - enough UCC-tagged courses to fill each UCC bucket's remaining credits
       - placeholder "elective" credits
  2. Repeatedly build terms. In each term, pick courses whose prereqs are
     already satisfied (by completed work OR earlier planned terms), that are
     offered that season, until the credit cap is hit.
  3. Prioritize courses that unlock the most downstream courses (highest
     out-degree in the prereq graph) so the critical path stays short.
"""
from __future__ import annotations
from app.models import (
    PlanRequest, PlanResponse, PlannedTerm, PlannedCourse,
)
from app.data.courses import COURSES
from app.data.degrees import DEGREES

SEASON_ORDER = ["Fall", "Spring", "Summer"]


def _next_term(season: str, year: int, include_summer: bool) -> tuple[str, int]:
    """Advance to the next schedulable season/year."""
    if season == "Fall":
        return ("Spring", year + 1)
    if season == "Spring":
        return ("Summer", year) if include_summer else ("Fall", year)
    # Summer
    return ("Fall", year)


def _prereqs_met(code: str, done: set[str]) -> bool:
    course = COURSES.get(code)
    if not course:
        return True
    for group in course.prereqs:
        if not any(opt in done for opt in group):
            return False
    return True


def _unlock_score(code: str, pending: set[str]) -> int:
    """How many pending courses list `code` as a prereq (out-degree)."""
    score = 0
    for other in pending:
        oc = COURSES.get(other)
        if not oc:
            continue
        for group in oc.prereqs:
            if code in group:
                score += 1
    return score


def build_plan(req: PlanRequest) -> PlanResponse:
    degree = DEGREES.get(req.degree_key)
    warnings: list[str] = []
    if degree is None:
        raise ValueError(f"Unknown degree: {req.degree_key}")

    completed_codes = {c.code for c in req.completed}
    completed_credits = sum(
        COURSES[c].credits for c in completed_codes if c in COURSES
    )

    # ---- 1. Determine what's still needed ----

    # a) Explicit required courses
    needed: set[str] = {
        c for c in degree.required_courses if c not in completed_codes
    }

    # b) UCC buckets — subtract credits already satisfied by completed courses
    ucc_filled: dict[str, int] = {u.key: 0 for u in degree.ucc_requirements}
    for code in completed_codes:
        course = COURSES.get(code)
        if not course:
            continue
        for tag in course.ucc_tags:
            if tag in ucc_filled:
                ucc_filled[tag] += course.credits

    # Choose UCC-filler courses for buckets not yet met.
    # (A required course may already cover a bucket — account for that too.)
    for code in needed:
        course = COURSES.get(code)
        if not course:
            continue
        for tag in course.ucc_tags:
            if tag in ucc_filled:
                ucc_filled[tag] += course.credits

    for ucc in degree.ucc_requirements:
        remaining = ucc.credits_required - ucc_filled[ucc.key]
        if remaining <= 0:
            continue
        # Pick candidate courses with this tag not already planned/completed.
        candidates = [
            code for code, c in COURSES.items()
            if ucc.key in c.ucc_tags
            and code not in completed_codes
            and code not in needed
        ]
        candidates.sort(key=lambda c: COURSES[c].credits, reverse=True)
        for code in candidates:
            if remaining <= 0:
                break
            needed.add(code)
            remaining -= COURSES[code].credits
        if remaining > 0:
            warnings.append(
                f"Not enough catalog courses to fill UCC '{ucc.name}' "
                f"({remaining} credits short) — add more options to the catalog."
            )

    # c) Free elective placeholder credits
    planned_named_credits = sum(COURSES[c].credits for c in needed if c in COURSES)
    elective_blocks: list[str] = []
    elective_remaining = degree.elective_credits
    idx = 1
    while elective_remaining > 0:
        block = min(3, elective_remaining)
        elective_blocks.append(f"ELECTIVE {idx} ({block} cr)")
        elective_remaining -= block
        idx += 1

    # ---- 2. Greedy term-by-term scheduling ----

    done = set(completed_codes)
    pending = set(needed)
    terms: list[PlannedTerm] = []
    season, year = req.start_term, req.start_year
    safety = 0

    while (pending or elective_blocks) and safety < 40:
        safety += 1
        term_label = f"{season} {year}"
        term_courses: list[PlannedCourse] = []
        term_credits = 0

        # Eligible = prereqs met AND offered this season
        eligible = [
            c for c in pending
            if _prereqs_met(c, done)
            and season in COURSES[c].offered
        ]
        # Prioritize courses that unlock the most downstream work.
        eligible.sort(key=lambda c: _unlock_score(c, pending), reverse=True)

        for code in eligible:
            credits = COURSES[code].credits
            if term_credits + credits > req.max_credits_per_term:
                continue
            term_courses.append(PlannedCourse(
                code=code,
                title=COURSES[code].title,
                credits=credits,
                reason=(
                    "Required course"
                    if code in degree.required_courses
                    else "Satisfies UCC / core requirement"
                ),
            ))
            term_credits += credits

        # Fill leftover room with elective blocks.
        while elective_blocks and term_credits < req.max_credits_per_term:
            label = elective_blocks[0]
            block_credits = int(label.split("(")[1].split(" ")[0])
            if term_credits + block_credits > req.max_credits_per_term:
                break
            elective_blocks.pop(0)
            term_courses.append(PlannedCourse(
                code=label, title="Free Elective",
                credits=block_credits, reason="Degree elective credits",
            ))
            term_credits += block_credits

        if not term_courses:
            # Deadlock guard: nothing schedulable (prereq cycle or offering gap).
            if pending:
                blocked = ", ".join(sorted(pending))
                warnings.append(
                    f"Could not schedule remaining courses ({blocked}); "
                    f"check for prerequisite cycles or offering constraints."
                )
            break

        for pc in term_courses:
            if pc.code in pending:
                pending.discard(pc.code)
                done.add(pc.code)

        terms.append(PlannedTerm(
            term=term_label, courses=term_courses, credits=term_credits,
        ))
        season, year = _next_term(season, year, req.include_summer)

    remaining_credits = max(0, degree.total_credits - completed_credits)

    return PlanResponse(
        degree=degree.name,
        terms=terms,
        total_terms=len(terms),
        completed_credits=completed_credits,
        remaining_credits=remaining_credits,
        warnings=warnings,
    )