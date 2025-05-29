import pytest
from django.core.asgi import get_asgi_application
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_positive_when_valid_job_payload_then_job_is_created_successfully(auth_header):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.post(
            "/api/job/",
            json={
                "title": "Backend Engineer",
                "description": "Build scalable backend services",
                "location": "Taipei",
                "salary_range": {"min": 90000, "max": 120000},
                "company_name": "TechNova",
                "posting_date": "2024-01-01",
                "expiration_date": "2024-12-31",
                "required_skills": ["Python", "Django"],
                "status": "active",
            },
        )
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Backend Engineer"
        assert data["company_name"] == "TechNova"
        assert data["status"] == "active"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_positive_when_valid_job_id_then_job_is_retrieved_successfully(auth_header, created_job_id):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.get(f"/api/job/{created_job_id.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(created_job_id.id)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_positive_when_valid_update_payload_then_job_is_updated_successfully(auth_header, created_job_id):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.put(
            f"/api/job/{created_job_id.id}",
            json={
                "title": "Updated Title",
                "description": "Updated description",
                "location": "Taipei",
                "salary_range": {"min": 50000, "max": 100000},
                "posting_date": "2024-01-01",
                "expiration_date": "2024-12-31",
                "required_skills": ["Python"],
                "status": "scheduled",
            },
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_positive_when_valid_job_id_then_job_is_deleted_successfully(auth_header, created_job_id):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.delete(f"/api/job/{created_job_id.id}")
        assert response.status_code == 204


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_positive_when_multiple_jobs_exist_then_job_list_is_returned(auth_header, create_multiple_jobs):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.get("/api/job/", params={"page": 1, "page_size": 10})

    # Assert
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert isinstance(data["list"], list)
    assert len(data["list"]) > 0


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_positive_when_filter_by_active_status_then_only_active_jobs_are_returned(
    auth_header, create_multiple_jobs
):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.get("/api/job/", params={"page": 1, "page_size": 10, "status": "active"})

    # Assert
    assert response.status_code == 200
    data = response.json()
    for job in data["list"]:
        assert job["status"] == "active"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_positive_when_search_keyword_is_given_then_matched_jobs_are_returned(auth_header, create_multiple_jobs):

    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.get("/api/job/", params={"page": 1, "page_size": 10, "search": "Backend"})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["list"]) > 0
    assert any("Backend" in job["title"] for job in data["list"])


"""Negative test cases for job APIs"""

invalid_payloads = [
    ({}, "missing all fields"),
    (
        {
            "title": "Backend",
            "location": "Taipei",
            "salary_range": {"min": 90000, "max": 110000},
            "company_name": "TestCo",
            "posting_date": "2024-01-01",
            "expiration_date": "2024-12-31",
            "required_skills": ["Python"],
            "status": "active",
        },
        "missing description",
    ),
    (
        {
            "title": "Backend",
            "description": "Build stuff",
            "location": "Taipei",
            "salary_range": {"min": 100000, "max": 90000},
            "company_name": "TestCo",
            "posting_date": "2024-12-31",
            "expiration_date": "2024-01-01",
            "required_skills": ["Python"],
            "status": "active",
        },
        "expiration_date < posting_date",
    ),
    (
        {
            "title": "Backend",
            "description": "Build stuff",
            "location": "Taipei",
            "salary_range": {"min": 90000, "max": 110000},
            "company_name": "TestCo",
            "posting_date": "2024-01-01",
            "expiration_date": "2024-12-31",
            "required_skills": ["Python"],
            "status": "nonsense",
        },
        "invalid status enum",
    ),
]


@pytest.mark.asyncio
@pytest.mark.django_db
@pytest.mark.parametrize("payload,case", invalid_payloads)
async def test_negative_when_invalid_job_payload_then_API_returns_422(auth_header, payload, case):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.post("/api/job/", json=payload)
        assert response.status_code == 422, f"{case} did not return 422"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_negative_when_create_job_with_unexpected_field_then_return_422(auth_header):

    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    payload = {
        "title": "DevOps",
        "description": "Infra tasks",
        "location": "Taipei",
        "salary_range": {"min": 50000, "max": 70000},
        "company_name": "TestCo",
        "posting_date": "2024-01-01",
        "expiration_date": "2024-12-31",
        "required_skills": ["Linux", "AWS"],
        "status": "active",
        "unexpected_field": "not allowed",
    }

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.post("/api/job/", json=payload)
        assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_negative_when_get_job_by_non_existent_job_id_then_API_returns_404(auth_header):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    unknown_uuid = "00000000-0000-0000-0000-000000000000"

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.get(f"/api/job/{unknown_uuid}")
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_negative_when_delete_by_non_existent_job_id_then_API_returns_404(auth_header):
    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    unknown_uuid = "00000000-0000-0000-0000-000000000000"

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as client:
        response = await client.delete(f"/api/job/{unknown_uuid}")
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_negative_when_missing_token_then_API_returns_401():

    # Mock
    app = get_asgi_application()
    transport = ASGITransport(app=app)

    # Arrange
    payload = {
        "title": "Fullstack",
        "description": "Handle everything",
        "location": "Taipei",
        "salary_range": {"min": 100000, "max": 150000},
        "company_name": "TestCo",
        "posting_date": "2024-01-01",
        "expiration_date": "2024-12-31",
        "required_skills": ["Vue", "Django"],
        "status": "active",
    }

    # Act & Assert
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/job/", json=payload)
        assert response.status_code == 401
