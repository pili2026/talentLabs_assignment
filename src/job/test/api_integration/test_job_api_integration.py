from datetime import date
from uuid import uuid4

import pytest

from job.enum_type import JobStatusEnum
from job.model import JobDBModel
from job.schema.salary import SalaryRange


@pytest.mark.django_db
def test_create_job():
    job = JobDBModel.objects.create(
        id=uuid4(),
        title="Backend Engineer",
        description="Build APIs",
        location="Taipei",
        salary_range=SalaryRange(min=90000, max=110000).model_dump(mode="json"),
        company_name="TechNova",
        posting_date=date(2024, 1, 1),
        expiration_date=date(2024, 12, 31),
        required_skills=["Python", "Django"],
        status=JobStatusEnum.ACTIVE,
    )

    assert job.id is not None
    assert job.title == "Backend Engineer"
    assert job.status == JobStatusEnum.ACTIVE


@pytest.mark.django_db
def test_get_job_by_id():
    job = JobDBModel.objects.create(
        id=uuid4(),
        title="Frontend Developer",
        description="Build UI",
        location="Taipei",
        salary_range=SalaryRange(min=90000, max=110000).model_dump(mode="json"),
        company_name="UIWorks",
        posting_date=date(2024, 3, 1),
        expiration_date=date(2024, 12, 1),
        required_skills=["Vue", "TypeScript"],
        status=JobStatusEnum.ACTIVE,
    )

    found = JobDBModel.objects.get(id=job.id)
    assert found.title == "Frontend Developer"
    assert "Vue" in found.required_skills


@pytest.mark.django_db
def test_list_all_jobs():
    JobDBModel.objects.bulk_create(
        [
            JobDBModel(
                id=uuid4(),
                title=f"Job {i}",
                description="Some job",
                location="Remote",
                salary_range=SalaryRange(min=90000, max=110000).model_dump(mode="json"),
                company_name="JobCorp",
                posting_date=date(2024, 2, 1),
                expiration_date=date(2024, 12, 1),
                required_skills=["Python"],
                status=JobStatusEnum.SCHEDULED,
            )
            for i in range(3)
        ]
    )

    all_jobs = JobDBModel.objects.all()
    assert len(all_jobs) >= 3


@pytest.mark.django_db
def test_update_job():
    job = JobDBModel.objects.create(
        id=uuid4(),
        title="QA Engineer",
        description="Test stuff",
        location="Kaohsiung",
        salary_range=SalaryRange(min=90000, max=110000).model_dump(mode="json"),
        company_name="QATech",
        posting_date=date(2024, 4, 1),
        expiration_date=date(2024, 12, 1),
        required_skills=["Testing"],
        status=JobStatusEnum.EXPIRED,
    )

    job.title = "Senior QA Engineer"
    job.status = JobStatusEnum.ACTIVE
    job.save()

    updated = JobDBModel.objects.get(id=job.id)
    assert updated.title == "Senior QA Engineer"
    assert updated.status == JobStatusEnum.ACTIVE


@pytest.mark.django_db
def test_delete_job():
    job = JobDBModel.objects.create(
        id=uuid4(),
        title="Delete Me",
        description="This will be deleted",
        location="Taipei",
        salary_range=SalaryRange(min=90000, max=110000).model_dump(mode="json"),
        company_name="DelCorp",
        posting_date=date(2024, 5, 1),
        expiration_date=date(2024, 12, 1),
        required_skills=[],
        status=JobStatusEnum.SCHEDULED,
    )

    job_id = job.id
    job.delete()

    with pytest.raises(JobDBModel.DoesNotExist):
        JobDBModel.objects.get(id=job_id)
