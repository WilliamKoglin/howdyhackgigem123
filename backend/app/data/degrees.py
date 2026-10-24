"""
Texas A&M degree definitions.

The data now lives in app/data/catalog/degrees.json — edit that file to add
or change degrees. Use "ucc_requirements": "STANDARD" for the standard 42-hour
core, or supply a full list of UCC requirement objects for a custom core.
This module just loads it; `DEGREES` is the public interface.
"""
from app.data.loader import load_degrees

DEGREES = load_degrees()