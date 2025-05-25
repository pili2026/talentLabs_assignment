from uuid import uuid4

import pytest
from django.core.asgi import get_asgi_application
from httpx import ASGITransport, AsyncClient

from job.exception import NotFoundException
from job.schema import JobCreate, JobUpdate


@pytest.mark.asyncio
async def test_positive_create_job_api(mocker, fake_job_response):
    # Mock
    mocker.patch("job.repository.JobRepository.create", return_value=fake_job_response)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = JobCreate(**fake_job_response.model_dump()).model_dump(mode="json")

        response = await client.post("/api/job/", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["title"] == "Engineer"


@pytest.mark.asyncio
async def test_positive_get_job_by_id_api(mocker, fake_job_response):
    # Mock
    mocker.patch("job.repository.JobRepository.get_by_id", return_value=fake_job_response)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/job/{fake_job_response.id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == str(fake_job_response.id)


@pytest.mark.asyncio
async def test_positive_list_all_jobs_api(mocker, fake_job_response):
    # Mock
    mocker.patch("job.repository.JobRepository.get_all", return_value=[fake_job_response])

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/job/")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == "Engineer"


@pytest.mark.asyncio
async def test_positive_update_job_api(mocker, fake_job_response):
    # Mock
    mocker.patch("job.repository.JobRepository.update", return_value=fake_job_response)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = JobUpdate(**fake_job_response.model_dump()).model_dump(mode="json")

        response = await client.put(f"/api/job/{fake_job_response.id}", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == str(fake_job_response.id)


@pytest.mark.asyncio
async def test_positive_delete_job_api(mocker, fake_job_response):
    # Mock
    mocker.patch("job.repository.JobRepository.delete", return_value=True)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(f"/api/job/{fake_job_response.id}")

    # Assert
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_negative_create_job_when_missing_fields():
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/job/",
            json={"title": "Engineer"},
        )

    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_negative_create_job_when_invalid_enum():
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
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
async def test_negative_get_job_when_not_found(mocker):
    # Mock
    mocker.patch("job.repository.JobRepository.get_by_id", side_effect=NotFoundException("Not found"))

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/job/{uuid4()}")

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_negative_update_job_when_not_found(mocker, fake_job_response):
    # Mock
    mocker.patch("job.repository.JobRepository.update", side_effect=NotFoundException("Not found"))

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = JobUpdate(**fake_job_response.model_dump()).model_dump(mode="json")
        response = await client.put(f"/api/job/{uuid4()}", json=payload)

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_negative_delete_job_when_not_found(mocker):
    # Mock
    mocker.patch("job.repository.JobRepository.delete", return_value=False)

    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(f"/api/job/{uuid4()}")

    # Assert
    assert response.status_code == 404
