import django
import pytest
from django.contrib.auth.models import User
from django.core.asgi import get_asgi_application
from ninja_jwt.authentication import JWTAuth


@pytest.fixture(scope="session")
def asgi_django_app():
    django.setup()
    return get_asgi_application()


@pytest.fixture
def mock_auth_user(mocker):
    mock_user = User(id=1, username="test_user", is_active=True)
    mocker.patch.object(JWTAuth, "authenticate", return_value=mock_user)
    return mock_user
