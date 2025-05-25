from uuid import uuid4

import pytest
from django.core.asgi import get_asgi_application
from httpx import ASGITransport, AsyncClient

from job.enum_type import JobStatusEnum
from job.exception import NotFoundException
from job.schema import JobCreate, JobUpdate, PaginationResult

"""Positive test cases for job handler APIs"""


@pytest.mark.asyncio
async def test_positive_create_job_api(mocker, fake_job_response, mock_auth_user):
    # Mock
    mocker.patch("job.repository.JobRepository.create", return_value=fake_job_response)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    request_body = JobCreate(**fake_job_response.model_dump()).model_dump(mode="json")
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.post("/api/job/", json=request_body)

    # Assert
    assert response.status_code == 200
    assert response.json()["title"] == "Engineer"


@pytest.mark.asyncio
async def test_positive_get_job_by_id_api(mocker, fake_job_response, mock_auth_user):
    # Mock
    mocker.patch("job.repository.JobRepository.get_by_id", return_value=fake_job_response)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.get(f"/api/job/{fake_job_response.id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == str(fake_job_response.id)


@pytest.mark.asyncio
async def test_positive_list_all_job(mocker, fake_job_response, mock_auth_user):
    # Mock
    pagination_result = PaginationResult(
        total=1,
        page=1,
        page_size=10,
        list=[fake_job_response],
    )

    mocker.patch("job.repository.JobRepository.get_all", return_value=pagination_result)

    app = get_asgi_application()
    transport = ASGITransport(app=app)
    headers = {"Authorization": "Bearer faketoken"}

    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.get("/api/job/?page=1&page_size=10")

    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert isinstance(data["list"], list)
    assert data["list"][0]["title"] == fake_job_response.title


@pytest.mark.asyncio
async def test_positive_update_job_api(mocker, fake_job_response, mock_auth_user):
    # Mock
    mocker.patch("job.repository.JobRepository.update", return_value=fake_job_response)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}
    request_body = JobUpdate(**fake_job_response.model_dump()).model_dump(mode="json")

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.put(f"/api/job/{fake_job_response.id}", json=request_body)

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == str(fake_job_response.id)


@pytest.mark.asyncio
async def test_positive_delete_job_api(mocker, fake_job_response, mock_auth_user):
    # Mock
    mocker.patch("job.repository.JobRepository.delete", return_value=True)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.delete(f"/api/job/{fake_job_response.id}")

    # Assert
    assert response.status_code == 204


"""Negative test cases for job handler APIs"""


@pytest.mark.asyncio
async def test_negative_create_job_when_missing_fields(mock_auth_user):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.post(
            "/api/job/",
            json={"title": "Engineer"},
        )

    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_negative_create_job_when_invalid_enum(mock_auth_user):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.post(
            "/api/job/",
            json={
                "title": "Engineer",
                "description": "Build things",
                "location": "Taipei",
                "salary_range": "80k-100k",
                "company_name": "Test Co",
                "posting_date": "2024-01-01",
                "expiration_date": "2024-12-31",
                "required_skills": ["Python"],
                "status": "WRONG_ENUM",
            },
        )

    # Assert
    assert response.status_code == 422
    assert "status" in str(response.json())


@pytest.mark.asyncio
async def test_negative_get_job_when_not_found(mocker, mock_auth_user):
    # Mock
    mocker.patch("job.repository.JobRepository.get_by_id", side_effect=NotFoundException("Not found"))

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.get(f"/api/job/{uuid4()}")

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_negative_update_job_when_not_found(mocker, fake_job_response, mock_auth_user):
    # Mock
    mocker.patch("job.repository.JobRepository.update", side_effect=NotFoundException("Not found"))

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}
    request_body = JobUpdate(**fake_job_response.model_dump()).model_dump(mode="json")

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.put(f"/api/job/{uuid4()}", json=request_body)

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_negative_delete_job_when_not_found(mocker, mock_auth_user):
    # Mock
    mocker.patch("job.repository.JobRepository.delete", return_value=False)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.delete(f"/api/job/{uuid4()}")

    # Assert
    assert response.status_code == 404


"""Additional test cases for job handler APIs"""


@pytest.mark.asyncio
async def test_list_jobs_by_search_engineer(mocker, multiple_fake_jobs, mock_auth_user):

    # Mock
    matched = [job for job in multiple_fake_jobs if "engineer" in job.title.lower()]

    mocker.patch(
        "job.repository.JobRepository.get_all",
        return_value=PaginationResult(total=len(matched), page=1, page_size=10, list=matched),
    )

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.get("/api/job/?search=engineer&page=1&page_size=10")

    # Assert
    assert response.status_code == 200
    assert all("engineer" in job["title"].lower() for job in response.json()["list"])


@pytest.mark.asyncio
async def test_list_jobs_by_status_active(mocker, multiple_fake_jobs, mock_auth_user):
    # Mock
    filtered = [job for job in multiple_fake_jobs if job.status == JobStatusEnum.ACTIVE]

    mocker.patch(
        "job.repository.JobRepository.get_all",
        return_value=PaginationResult(total=len(filtered), page=1, page_size=10, list=filtered),
    )

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.get("/api/job/?status=active&page=1&page_size=10")

    # Assert
    assert response.status_code == 200
    assert all(job["status"] == "active" for job in response.json()["list"])


@pytest.mark.asyncio
async def test_list_jobs_sorted_by_posting_date_asc(mocker, multiple_fake_jobs, mock_auth_user):
    # Mock
    sorted_list = sorted(multiple_fake_jobs, key=lambda j: j.posting_date)

    mocker.patch(
        "job.repository.JobRepository.get_all",
        return_value=PaginationResult(total=len(sorted_list), page=1, page_size=10, list=sorted_list),
    )

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    headers = {"Authorization": "Bearer faketoken"}

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        response = await client.get("/api/job/?order_by=posting_date&sort_order=asc")

    # Assert
    assert response.status_code == 200

    jobs = response.json()["list"]
    post_dates = [job["posting_date"] for job in jobs]
    assert post_dates == sorted(post_dates)
