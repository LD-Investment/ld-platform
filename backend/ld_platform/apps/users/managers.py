from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    def _create_user(
        self, email, username, first_name, last_name, password, **extra_fields
    ):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        validate_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email, username, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields
        )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        first_name = extra_fields.pop("first_name", "admin")
        last_name = extra_fields.pop("last_name", "L&D")
        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields
        )
