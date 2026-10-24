"""
Texas A&M course catalog.

The data now lives in app/data/catalog/courses.json — edit that file to add
or change courses. This module just loads it. The `COURSES` dict (keyed by
course code) is the public interface the rest of the app imports.
"""
from app.data.loader import load_courses

COURSES = load_courses()