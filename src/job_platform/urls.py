from authentication.handler import PrivateAuthController, PublicAuthController
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from ninja_extra import NinjaExtraAPI

from job.exception import NotFoundException
from job.handler import job_router

api = NinjaExtraAPI()


@api.exception_handler(NotFoundException)
def not_found_handler(request, exc: NotFoundException):
    return JsonResponse({"detail": str(exc)}, status=404)


api.add_router("/job", job_router)
api.register_controllers(PublicAuthController)
api.register_controllers(PrivateAuthController)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
