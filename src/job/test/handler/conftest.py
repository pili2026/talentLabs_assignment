import pytest
from asgiref.compatibility import guarantee_single_callable
from httpx import ASGITransport, AsyncClient
from job_platform.asgi import application


@pytest.fixture
async def httpx_async_client():
    app = guarantee_single_callable(application)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
