from datetime import datetime, timedelta
from uuid import uuid4

import django
import pytest
from django.contrib.auth.models import User
from django.core.asgi import get_asgi_application
from ninja_jwt.authentication import JWTAuth

from job.enum_type import JobStatusEnum
from job.schema import JobResponse


@pytest.fixture(scope="session")
def asgi_django_app():
    django.setup()
    return get_asgi_application()


@pytest.fixture
def mock_auth_user(mocker):
    mock_user = User(id=1, username="test_user", is_active=True)
    mocker.patch.object(JWTAuth, "authenticate", return_value=mock_user)
    return mock_user


@pytest.fixture
def multiple_fake_jobs() -> list[JobResponse]:
    now = datetime.now()

    return [
        JobResponse(
            id=uuid4(),
            title="Backend Engineer",
            description="Build APIs",
            location="Taipei",
            salary_range="80k-100k",
            posting_date=(now - timedelta(days=10)).date(),
            expiration_date=(now + timedelta(days=10)).date(),
            required_skills=["Python"],
            status=JobStatusEnum.ACTIVE,
            company_name="Tech Co",
        ),
        JobResponse(
            id=uuid4(),
            title="Frontend Engineer",
            description="React frontend",
            location="Kaohsiung",
            salary_range="70k-90k",
            posting_date=(now - timedelta(days=20)).date(),
            expiration_date=(now - timedelta(days=2)).date(),
            required_skills=["JavaScript"],
            status=JobStatusEnum.EXPIRED,
            company_name="Frontend Inc",
        ),
        JobResponse(
            id=uuid4(),
            title="DevOps Engineer",
            description="CI/CD pipelines",
            location="Tainan",
            salary_range="90k-120k",
            posting_date=(now - timedelta(days=5)).date(),
            expiration_date=(now + timedelta(days=25)).date(),
            required_skills=["Docker", "K8s"],
            status=JobStatusEnum.ACTIVE,
            company_name="CloudOps",
        ),
        JobResponse(
            id=uuid4(),
            title="AI Researcher",
            description="Work with LLMs",
            location="Taipei",
            salary_range="150k-180k",
            posting_date=(now - timedelta(days=3)).date(),
            expiration_date=(now + timedelta(days=30)).date(),
            required_skills=["Python", "ML"],
            status=JobStatusEnum.SCHEDULED,
            company_name="AI Lab",
        ),
        JobResponse(
            id=uuid4(),
            title="QA Engineer",
            description="Write test cases",
            location="Hsinchu",
            salary_range="60k-80k",
            posting_date=(now - timedelta(days=15)).date(),
            expiration_date=(now - timedelta(days=1)).date(),
            required_skills=["Selenium"],
            status=JobStatusEnum.EXPIRED,
            company_name="Quality Matters",
        ),
        JobResponse(
            id=uuid4(),
            title="Data Analyst",
            description="Analyze sales data",
            location="Taipei",
            salary_range="70k-100k",
            posting_date=(now - timedelta(days=8)).date(),
            expiration_date=(now + timedelta(days=12)).date(),
            required_skills=["SQL", "Excel"],
            status=JobStatusEnum.ACTIVE,
            company_name="DataCo",
        ),
        JobResponse(
            id=uuid4(),
            title="Fullstack Developer",
            description="React + Django",
            location="Taichung",
            salary_range="100k-130k",
            posting_date=(now - timedelta(days=7)).date(),
            expiration_date=(now + timedelta(days=14)).date(),
            required_skills=["React", "Django"],
            status=JobStatusEnum.ACTIVE,
            company_name="StackTech",
        ),
        JobResponse(
            id=uuid4(),
            title="Project Manager",
            description="Manage software projects",
            location="Taipei",
            salary_range="90k-110k",
            posting_date=(now - timedelta(days=12)).date(),
            expiration_date=(now + timedelta(days=5)).date(),
            required_skills=["Agile"],
            status=JobStatusEnum.ACTIVE,
            company_name="ManageIt",
        ),
        JobResponse(
            id=uuid4(),
            title="UX Designer",
            description="Design UI/UX",
            location="Kaohsiung",
            salary_range="80k-100k",
            posting_date=(now - timedelta(days=18)).date(),
            expiration_date=(now - timedelta(days=3)).date(),
            required_skills=["Figma"],
            status=JobStatusEnum.EXPIRED,
            company_name="Creative Studio",
        ),
        JobResponse(
            id=uuid4(),
            title="Technical Writer",
            description="Write docs",
            location="Remote",
            salary_range="60k-90k",
            posting_date=(now - timedelta(days=1)).date(),
            expiration_date=(now + timedelta(days=20)).date(),
            required_skills=["Markdown"],
            status=JobStatusEnum.SCHEDULED,
            company_name="WriteWell",
        ),
    ]
