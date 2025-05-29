from datetime import date, timedelta
from uuid import uuid4

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from ninja_jwt.tokens import RefreshToken

from job.model import JobDBModel


@pytest.fixture
async def auth_header():
    User = get_user_model()
    user, created = await sync_to_async(User.objects.get_or_create)(
        username="admin",
        defaults={"is_active": True, "is_staff": True, "is_superuser": True},
    )
    if created:
        user.set_password("admin123")
        await sync_to_async(user.save)()

    refresh = RefreshToken.for_user(user)
    refresh.set_exp(lifetime=timedelta(days=1))
    access = refresh.access_token
    access.set_exp(lifetime=timedelta(minutes=10))

    return {"Authorization": f"Bearer {str(access)}"}


@pytest.fixture
async def created_job_id():
    job = await sync_to_async(JobDBModel.objects.create)(
        id=uuid4(),
        title="Test Job",
        description="Fixture created job",
        location="Taipei",
        salary_range={"min": 50000, "max": 70000},
        company_name="TestCo",
        posting_date=date(2024, 1, 1),
        expiration_date=date(2024, 12, 31),
        required_skills=["Python", "Django"],
        status="active",
    )
    return job


@pytest.fixture
def create_multiple_jobs():
    from job.model import JobDBModel

    for i in range(5):
        JobDBModel.objects.create(
            title=f"Job {i}",
            description="Integration Test",
            location="Taipei",
            salary_range={"min": 80000, "max": 100000},
            company_name="Test Co",
            posting_date=date(2024, 1, 1),
            expiration_date=date(2024, 12, 31),
            required_skills=["Python", "Django"],
            status="active",
        )
