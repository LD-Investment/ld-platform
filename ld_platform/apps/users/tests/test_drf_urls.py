import pytest
from django.urls import resolve, reverse

from ld_platform.apps.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("api:users:user-detail", kwargs={"user_id": user.id})
        == f"/api/users/{user.id}/"
    )
    assert resolve(f"/api/users/{user.id}/").view_name == "api:users:user-detail"


def test_user_list():
    assert reverse("api:users:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:users:user-list"
