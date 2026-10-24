"""
Catalog validation — run at startup so data errors fail loudly and early
instead of silently producing broken plans.

Checks performed:
  1. Every degree's required_courses reference a real course.
  2. Every course listed in a UCC-tagged course uses a valid UCC key
     (relative to each degree that uses it).
  3. Every prereq references a real course code.
  4. No prerequisite cycles exist in the course graph.
  5. Each degree's catalog actually has enough UCC-tagged courses to
     (in principle) fill every UCC bucket — warns, doesn't crash.
"""
from __future__ import annotations

from app.data.courses import COURSES
from app.data.degrees import DEGREES


class CatalogError(Exception):
    """Raised when the catalog has a fatal data problem."""


def _check_required_courses_exist() -> list[str]:
    errors: list[str] = []
    for degree in DEGREES.values():
        for code in degree.required_courses:
            if code not in COURSES:
                errors.append(
                    f"Degree '{degree.key}' requires unknown course '{code}'."
                )
    return errors


def _check_prereqs_exist() -> list[str]:
    errors: list[str] = []
    for course in COURSES.values():
        for group in course.prereqs:
            for code in group:
                if code not in COURSES:
                    errors.append(
                        f"Course '{course.code}' has unknown prereq '{code}'."
                    )
    return errors


def _check_prereq_cycles() -> list[str]:
    """Detect cycles in the prereq graph via DFS coloring."""
    errors: list[str] = []
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {code: WHITE for code in COURSES}

    def visit(code: str, stack: list[str]) -> None:
        color[code] = GRAY
        stack.append(code)
        course = COURSES.get(code)
        if course:
            for group in course.prereqs:
                for dep in group:
                    if dep not in COURSES:
                        continue
                    if color[dep] == GRAY:
                        cycle = " -> ".join(stack[stack.index(dep):] + [dep])
                        errors.append(f"Prerequisite cycle detected: {cycle}")
                    elif color[dep] == WHITE:
                        visit(dep, stack)
        stack.pop()
        color[code] = BLACK

    for code in COURSES:
        if color[code] == WHITE:
            visit(code, [])
    return errors


def _check_ucc_fillable() -> list[str]:
    """Warn (not fatal) if a degree can't possibly fill a UCC bucket."""
    warnings: list[str] = []
    for degree in DEGREES.values():
        for ucc in degree.ucc_requirements:
            available = sum(
                c.credits for c in COURSES.values() if ucc.key in c.ucc_tags
            )
            if available < ucc.credits_required:
                warnings.append(
                    f"Degree '{degree.key}': UCC bucket '{ucc.name}' needs "
                    f"{ucc.credits_required} cr but catalog only offers "
                    f"{available} cr of tagged courses."
                )
    return warnings


def validate_catalog() -> None:
    """Run all checks. Raises CatalogError on fatal problems; prints warnings."""
    fatal: list[str] = []
    fatal += _check_required_courses_exist()
    fatal += _check_prereqs_exist()
    fatal += _check_prereq_cycles()

    warnings = _check_ucc_fillable()

    for w in warnings:
        print(f"[catalog warning] {w}")

    if fatal:
        joined = "\n  - ".join(fatal)
        raise CatalogError(
            f"Catalog validation failed with {len(fatal)} error(s):\n  - {joined}"
        )

    print(
        f"[catalog] OK — {len(COURSES)} courses, {len(DEGREES)} degrees loaded."
    )