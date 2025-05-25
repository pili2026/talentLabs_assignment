from unittest.mock import AsyncMock

import pytest

from job.service import JobService


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def job_service(mock_repository):
    return JobService(job_repository=mock_repository)
