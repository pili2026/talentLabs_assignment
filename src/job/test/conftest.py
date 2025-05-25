from datetime import date
from uuid import UUID, uuid4

import pytest

from job.enum_type import JobStatusEnum
from job.schema import JobCreate, JobResponse


@pytest.fixture
def fake_job_response(existing_job_uuid) -> JobResponse:
    return JobResponse(
        id=existing_job_uuid,
        title="Engineer",
        description="Build APIs",
        location="Taipei",
        salary_range="80k-100k",
        company_name="Test Co",
        posting_date=date(2024, 1, 1),
        expiration_date=date(2024, 12, 31),
        required_skills=["Python", "Django"],
        status=JobStatusEnum.ACTIVE,
    )


@pytest.fixture
def stub_job_create_data() -> JobCreate:
    return JobCreate(
        title="Full Stack Engineer",
        description="Build APIs",
        location="Taipei",
        salary_range="Negotiable",
        company_name="talentlabs",
        posting_date=date(2024, 1, 1),
        expiration_date=date(2024, 12, 31),
        required_skills=["Python", "Django"],
        status=JobStatusEnum.ACTIVE,
    )


@pytest.fixture
def fake_job_update_data() -> JobCreate:
    return JobCreate(
        title="Updated Title",
        description="Updated Description",
        location="Remote",
        salary_range="100k-150k",
        company_name="UpdatedCorp",
        posting_date=date(2024, 2, 1),
        expiration_date=date(2024, 12, 31),
        required_skills=["FastAPI", "PostgreSQL"],
        status=JobStatusEnum.ACTIVE,
    )


@pytest.fixture
def fake_missing_field_data() -> dict:
    return {
        "description": "Missing title",
        "location": "Taipei",
        "salary_range": "Negotiable",
        "company_name": "talentlabs",
        "posting_date": date(2024, 1, 1),
        "expiration_date": date(2024, 12, 31),
        "required_skills": ["Python", "Django"],
        "status": JobStatusEnum.ACTIVE,
    }


@pytest.fixture
def existing_job_uuid() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


@pytest.fixture
def nonexistent_job_uuid() -> UUID:
    return UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def random_nonexistent_uuid() -> UUID:
    return uuid4()
