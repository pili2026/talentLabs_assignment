from typing import Optional

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja import Schema
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from pydantic import EmailStr, constr


class RegisterInput(Schema):
    username: constr(min_length=3, max_length=32)
    password: constr(min_length=6)
    email: Optional[EmailStr] = None


class RegisterResponse(Schema):
    id: int
    username: str
    email: Optional[str]


@api_controller("/auth", tags=["auth"])
class PublicAuthController(NinjaJWTDefaultController):

    @route.post("/register", auth=None, url_name="register")
    def register(self, request: HttpRequest, data: RegisterInput) -> RegisterResponse:
        if User.objects.filter(username=data.username).exists():
            raise ValueError("Username already exists")

        user = User.objects.create(
            username=data.username,
            password=make_password(data.password),
            email=data.email,
            is_active=True,
        )
        return RegisterResponse(id=user.id, username=user.username, email=user.email)


@api_controller("/auth", tags=["auth"], auth=JWTAuth())
class PrivateAuthController:

    @route.get("/me", url_name="me")
    def me(self, request):
        user = request.user
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
