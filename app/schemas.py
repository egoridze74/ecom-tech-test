from pydantic import BaseModel, Field, field_validator
from datetime import date


class GradeRecord(BaseModel):
    date: date
    group_name: str = Field(..., min_length=1, max_length=255)
    student_name: str = Field(..., min_length=1, max_length=255)
    grade: int = Field(..., ge=1, le=5)

    @field_validator("group_name", "student_name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Имя студента и название группы должны быть непустыми")
        return v.strip()


class UploadResponse(BaseModel):
    status: str
    records_loaded: int
    students: int


class StudentTwos(BaseModel):
    full_name: str
    count_twos: int
