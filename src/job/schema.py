from datetime import date
from typing import Union
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict

from .enum_type import JobStatusEnum


class SalaryRangeObject(Schema):
    min: int | None = None
    max: int | None = None


class JobBase(Schema):
    title: str
    description: str
    location: str
    salary_range: Union[str, SalaryRangeObject]
    posting_date: date
    expiration_date: date
    required_skills: list[str]
    status: JobStatusEnum


class JobCreate(JobBase):
    company_name: str


class JobUpdate(JobBase):
    pass


class JobResponse(JobBase):
    id: UUID
    company_name: str

    model_config = ConfigDict(from_attributes=True)
