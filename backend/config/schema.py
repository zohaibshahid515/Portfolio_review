# app/api/schema.py
from pydantic import BaseModel

class SectionValidationResult(BaseModel):
    section: str
    validation: str  # "YES" or "NO"
    reason: str
