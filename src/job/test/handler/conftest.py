import django
import pytest
from django.core.asgi import get_asgi_application


@pytest.fixture(scope="session")
def asgi_django_app():
    django.setup()
    return get_asgi_application()
