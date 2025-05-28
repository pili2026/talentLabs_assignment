from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from job.exception import NotFoundException
from job.repository import JobRepository
from job.schema.job import (
    JobCreate,
    JobListQuery,
    JobResponse,
    JobSortField,
    JobStatusEnum,
    JobUpdate,
    SalaryRange,
    SortOrder,
)


@pytest.mark.asyncio
async def test_create_job_returns_service_model(mocker):
    # Mock
    mock_job_response = JobResponse(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        title="Test Job",
        description="desc",
        location="Taipei",
        salary_range=SalaryRange(min=80000, max=100000),
        company_name="Test Co",
        posting_date=date.today(),
        expiration_date=date.today(),
        required_skills=["Python"],
        status=JobStatusEnum.ACTIVE,
    )

    mock_created_job = MagicMock()
    mock_created_job.to_service_model.return_value = mock_job_response

    mock_objects = AsyncMock()
    mock_objects.acreate.return_value = mock_created_job

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    # Act
    job = JobCreate(
        title="Test Job",
        description="desc",
        location="Taipei",
        salary_range=SalaryRange(min=80000, max=100000),
        company_name="Test Co",
        posting_date=date.today(),
        expiration_date=date.today(),
        required_skills=["Python"],
        status=JobStatusEnum.ACTIVE,
    )

    result = await job_repository.create(job)

    # Assert
    mock_objects.acreate.assert_called_once()
    mock_created_job.to_service_model.assert_called_once()
    assert result.title == "Test Job"
    assert isinstance(result, JobResponse)


@pytest.mark.asyncio
async def test_get_by_id_returns_service_model(mocker):
    # Mock
    fake_job_id = UUID("00000000-0000-0000-0000-000000000002")
    mock_job_response = JobResponse(
        id=fake_job_id,
        title="Retrieved Job",
        description="desc",
        location="Taipei",
        salary_range=SalaryRange(min=80000, max=100000),
        company_name="Test Co",
        posting_date=date.today(),
        expiration_date=date.today(),
        required_skills=["Python"],
        status=JobStatusEnum.ACTIVE,
    )

    mock_job = MagicMock()
    mock_job.to_service_model.return_value = mock_job_response

    mock_objects = MagicMock()
    mock_objects.filter.return_value.first.return_value = mock_job

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    # Act
    result = await job_repository.get_by_id(fake_job_id)

    # Assert
    mock_objects.filter.assert_called_once()
    mock_job.to_service_model.assert_called_once()
    assert result.id == fake_job_id
    assert isinstance(result, JobResponse)


@pytest.mark.asyncio
async def test_update_job_returns_updated_service_model(mocker):
    # Mock
    fake_job_id = UUID("00000000-0000-0000-0000-000000000003")
    mock_job_response = JobResponse(
        id=fake_job_id,
        title="Updated Job",
        description="updated desc",
        location="Taipei",
        salary_range=SalaryRange(min=80000, max=100000),
        company_name="Test Co",
        posting_date=date.today(),
        expiration_date=date.today(),
        required_skills=["Python"],
        status=JobStatusEnum.ACTIVE,
    )

    mock_job = MagicMock()
    mock_job.asave = AsyncMock()
    mock_job.to_service_model.return_value = mock_job_response

    mock_objects = MagicMock()
    mock_objects.filter.return_value.first.return_value = mock_job

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    # Act
    update_data = JobUpdate(title="Updated Job")
    result = await job_repository.update(fake_job_id, update_data)

    # Assert
    mock_objects.filter.assert_called_once()
    mock_job.to_service_model.assert_called_once()
    assert result.title == "Updated Job"
    assert isinstance(result, JobResponse)


@pytest.mark.asyncio
async def test_delete_job_returns_true(mocker):
    # Mock
    fake_job_id = UUID("00000000-0000-0000-0000-000000000004")

    mock_filter_result = MagicMock()
    mock_filter_result.adelete = AsyncMock(return_value=(1, {}))

    mock_objects = MagicMock()
    mock_objects.filter.return_value = mock_filter_result

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    # Act
    result = await job_repository.delete(fake_job_id)

    # Assert
    mock_objects.filter.assert_called_once_with(id=fake_job_id)
    mock_filter_result.adelete.assert_called_once()
    assert result is True


@pytest.mark.asyncio
async def test_get_all_skill_returns_unique_skills(mocker):
    # Mock
    mock_objects = MagicMock()
    mock_objects.values_list.return_value = [["Python", "Vue"], ["Python", "Django"]]

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    # Act
    result = await job_repository.get_all_skill()

    # Assert
    mock_objects.values_list.assert_called_once()
    assert sorted(result) == ["Django", "Python", "Vue"]


@pytest.mark.asyncio
async def test_get_all_returns_paginated_jobs(mocker):
    # Mock
    fake_job_id = UUID("00000000-0000-0000-0000-000000000005")
    mock_job_response = JobResponse(
        id=fake_job_id,
        title="Query Job",
        description="query test",
        location="Taipei",
        salary_range=SalaryRange(min=80000, max=100000),
        company_name="Query Co",
        posting_date=date.today(),
        expiration_date=date.today(),
        required_skills=["Python"],
        status=JobStatusEnum.ACTIVE,
    )

    mock_job = MagicMock()
    mock_job.to_service_model.return_value = mock_job_response

    mock_qs = MagicMock()
    mock_qs.count.return_value = 1
    mock_qs.order_by.return_value = mock_qs
    mock_qs.__getitem__.return_value = [mock_job]

    mock_objects = MagicMock()
    mock_objects.filter.return_value = mock_qs

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    query = JobListQuery(
        page=1, page_size=10, order_by=JobSortField.POSTING_DATE, sort_order=SortOrder.ASC, search="Query Job"
    )

    # Act
    result = await job_repository.get_all(query)

    # Assert
    mock_objects.filter.assert_called_once()
    assert result.total == 1
    assert isinstance(result.list[0], JobResponse)


@pytest.mark.asyncio
async def test_get_all_with_no_filters(mocker):
    # Mock
    fake_job_id = UUID("00000000-0000-0000-0000-000000000005")
    mock_job = MagicMock()
    mock_job.to_service_model.return_value = JobResponse(
        id=fake_job_id,
        title="Default",
        description="",
        location="",
        salary_range="",
        company_name="",
        posting_date=date.today(),
        expiration_date=date.today(),
        required_skills=[],
        status=JobStatusEnum.ACTIVE,
    )

    mock_qs = MagicMock()
    mock_qs.count.return_value = 1
    mock_qs.order_by.return_value = mock_qs
    mock_qs.__getitem__.return_value = [mock_job]

    mock_objects = MagicMock()
    mock_objects.filter.return_value = mock_qs

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    # Act
    query = JobListQuery(page=1, page_size=10, order_by=JobSortField.POSTING_DATE, sort_order=SortOrder.DESC)
    result = await job_repository.get_all(query)

    # Assert
    assert result.total == 1
    assert isinstance(result.list[0], JobResponse)


@pytest.mark.asyncio
async def test_get_by_id_raises_not_found(mocker):
    # Mock
    fake_job_id = UUID("00000000-0000-0000-0000-00000000abcd")

    mock_objects = MagicMock()
    mock_objects.filter.return_value.first.return_value = None

    job_repository = JobRepository()
    mocker.patch.object(job_repository, "objects", mock_objects)

    # Act & Assert
    with pytest.raises(NotFoundException):
        await job_repository.get_by_id(fake_job_id)
