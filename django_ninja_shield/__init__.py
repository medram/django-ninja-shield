from __future__ import annotations

from typing import TYPE_CHECKING

from .base import AtomicOperation, P

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

"""
Here we define all needed permissions.
"""


class IsAdmin(AtomicOperation):
    """A permission operation that checks if the user is an admin"""

    def resolve(self, user: AbstractUser) -> bool:
        return user.is_superuser


class IsStaff(AtomicOperation):
    """A permission operation that checks if the user is a staff"""

    def resolve(self, user: AbstractUser) -> bool:
        return user.is_staff


class IsActive(AtomicOperation):
    """A permission operation that checks if the user is active"""

    def resolve(self, user: AbstractUser) -> bool:
        return user.is_active


__all__ = ["P", "IsAdmin", "IsStaff", "IsActive"]
