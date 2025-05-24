import pytest


@pytest.mark.asyncio
async def test_create_job_success_httpx(httpx_async_client, stub_job_create_data):
    response = await httpx_async_client.post("/api/job/", json=stub_job_create_data.model_dump(mode="json"))

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == stub_job_create_data.title


@pytest.mark.asyncio
async def test_create_job_fail_when_missing_field_httpx(httpx_async_client, stub_missing_field_data):
    response = await httpx_async_client.post("/api/job/", json=stub_missing_field_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_job_success_httpx(httpx_async_client, stub_job_create_data):
    create_res = await httpx_async_client.post("/api/job/", json=stub_job_create_data.model_dump(mode="json"))
    job_id = create_res.json()["id"]

    get_res = await httpx_async_client.get(f"/api/job/{job_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == job_id


@pytest.mark.asyncio
async def test_delete_job_success_httpx(httpx_async_client, stub_job_create_data):
    create_res = await httpx_async_client.post("/api/job/", json=stub_job_create_data.model_dump(mode="json"))
    job_id = create_res.json()["id"]

    delete_res = await httpx_async_client.delete(f"/api/job/{job_id}")
    assert delete_res.status_code == 204

    get_res = await httpx_async_client.get(f"/api/job/{job_id}")
    assert get_res.status_code == 404
