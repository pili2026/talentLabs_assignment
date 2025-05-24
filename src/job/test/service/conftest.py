import pytest

from job.repository import JobRepository
from job.service import JobService


@pytest.fixture
def job_service():
    return JobService(JobRepository())
