import pytest
from pydantic import ValidationError

from job.exception import NotFoundException
from job.schema import JobCreate, JobResponse


@pytest.mark.asyncio
async def test_positive_create_job_returns_job_response(
    existing_job_uuid, job_service, mock_repository, fake_job_create_data
):
    # Mock
    mock_repository.create.return_value = JobResponse(id=existing_job_uuid, **fake_job_create_data.model_dump())

    # Act
    result = await job_service.create_job(fake_job_create_data)

    # Assert
    assert isinstance(result, JobResponse)
    assert result.title == fake_job_create_data.title
    mock_repository.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_positive_get_job_returns_expected_result(
    existing_job_uuid, job_service, mock_repository, fake_job_create_data
):
    # Mock
    expected = JobResponse(id=existing_job_uuid, **fake_job_create_data.dict())
    mock_repository.get_by_id.return_value = expected

    # Act
    result = await job_service.get_job(existing_job_uuid)

    # Assert
    assert result.id == existing_job_uuid
    assert result.title == expected.title


@pytest.mark.asyncio
async def test_positive_update_job_returns_updated_result(
    existing_job_uuid, job_service, mock_repository, fake_job_update_data
):
    # Mock
    expected = JobResponse(id=existing_job_uuid, **fake_job_update_data.model_dump())
    mock_repository.update.return_value = expected

    # Act
    result = await job_service.update_job(existing_job_uuid, fake_job_update_data)

    # Assert
    assert result.title == fake_job_update_data.title
    mock_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_positive_delete_job_returns_true(existing_job_uuid, job_service, mock_repository):
    # Mock
    mock_repository.delete.return_value = True

    # Act
    result = await job_service.delete_job(existing_job_uuid)

    # Assert
    assert result is True
    mock_repository.delete.assert_awaited_once()


def test_negative_create_job_raises_validation_error_when_missing_field(fake_missing_field_data):
    # Act & Assert
    with pytest.raises(ValidationError):
        JobCreate(**fake_missing_field_data)


@pytest.mark.asyncio
async def test_negative_get_job_raises_not_found_when_missing(nonexistent_job_uuid, job_service, mock_repository):
    # Mock
    expected_msg = f"Job with id {nonexistent_job_uuid} not found"
    mock_repository.get_by_id.side_effect = NotFoundException(expected_msg)

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        await job_service.get_job(nonexistent_job_uuid)

    # Assert
    assert exc_info.value.args[0] == expected_msg


@pytest.mark.asyncio
async def test_negative_update_job_raises_not_found_when_missing(
    nonexistent_job_uuid, job_service, mock_repository, fake_job_update_data
):
    # Mock
    expected_msg = f"Job with id {nonexistent_job_uuid} not found"
    mock_repository.update.side_effect = NotFoundException(expected_msg)

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        await job_service.update_job(nonexistent_job_uuid, fake_job_update_data)

    assert exc_info.value.args[0] == expected_msg


@pytest.mark.asyncio
async def test_negative_delete_job_returns_false_when_not_found(nonexistent_job_uuid, job_service, mock_repository):
    # Mock
    mock_repository.delete.return_value = False

    # Act
    result = await job_service.delete_job(nonexistent_job_uuid)

    # Assert
    assert result is False
