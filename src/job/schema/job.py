from datetime import date
from enum import StrEnum
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict

from job.enum_type import JobStatusEnum
from job.schema.salary import SalaryRange


class JobBase(Schema):
    title: str
    description: str
    location: str
    salary_range: SalaryRange
    posting_date: date
    expiration_date: date
    required_skills: list[str]
    status: JobStatusEnum

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class JobCreate(JobBase):
    company_name: str


class JobUpdate(Schema):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    salary_range: SalaryRange | None = None
    posting_date: date | None = None
    expiration_date: date | None = None
    required_skills: list[str] | None = None
    status: JobStatusEnum | None = None

    model_config = ConfigDict(extra="forbid")


class JobResponse(JobBase):
    id: UUID
    company_name: str

    model_config = ConfigDict(from_attributes=True)


class JobSortField(StrEnum):
    POSTING_DATE = "posting_date"
    EXPIRATION_DATE = "expiration_date"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class JobListQuery(Schema):
    page: int = 1
    page_size: int = 10

    search: str | None = None

    status: JobStatusEnum | None = None
    location: str | None = None
    company_name: str | None = None
    skills: list[str] | None = None

    order_by: JobSortField | None = JobSortField.POSTING_DATE
    sort_order: SortOrder | None = SortOrder.DESC

    model_config = ConfigDict(extra="forbid")


class PaginationResult(Schema):
    total: int
    page: int
    page_size: int
    list: list[JobResponse]

    model_config = ConfigDict(from_attributes=True)
