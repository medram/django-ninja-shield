from __future__ import annotations

from typing import TYPE_CHECKING

from .base import AtomicOperation, P
from .decorators import requires_permissions

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

"""Django Ninja Shield - Permission handling for Django views.

This module provides a flexible permission system that allows combining multiple
permission checks using logical operations (AND, OR, NOT). It includes both
built-in permission checks for common Django user attributes (is_staff,
is_superuser, etc.) and support for custom permission operations.

Example:
    ```python
    from django_ninja_shield import IsAdmin, IsActive, requires_permissions
    
    # Simple permission check
    @requires_permissions(IsAdmin())
    def admin_view(request):
        ...
    
    # Complex permission check using logical operators
    @requires_permissions(IsActive() & (IsAdmin() | IsStaff()))
    def protected_view(request):
        ...
    ```
"""


class IsAdmin(AtomicOperation):
    """Permission check for Django superuser status.

    This permission operation checks if the user has superuser status
    (is_superuser=True) in Django. Superusers have all permissions by
    default in Django.

    Example:
        ```python
        # Require superuser status
        @requires_permissions(IsAdmin())
        def superuser_only(request):
            ...

        # Combine with other permissions
        @requires_permissions(IsAdmin() & IsActive())
        def active_admin_only(request):
            ...
        ```
    """

    def resolve(self, user: AbstractUser) -> bool:
        """Check if the user is a superuser.

        Args:
            user: The Django user to check

        Returns:
            True if the user is a superuser, False otherwise
        """
        return user.is_superuser


IsSuperuser = IsAdmin  # alias


class IsStaff(AtomicOperation):
    """Permission check for Django staff status.

    This permission operation checks if the user has staff status
    (is_staff=True) in Django. Staff users typically have access to
    the Django admin interface.

    Example:
        ```python
        # Allow either staff or admin access
        @requires_permissions(IsStaff() | IsAdmin())
        def staff_or_admin(request):
            ...
        ```
    """

    def resolve(self, user: AbstractUser) -> bool:
        """Check if the user is staff.

        Args:
            user: The Django user to check

        Returns:
            True if the user is staff, False otherwise
        """
        return user.is_staff


class IsActive(AtomicOperation):
    """Permission check for Django active user status.

    This permission operation checks if the user account is active
    (is_active=True) in Django. Inactive users are typically treated
    as if they have no permissions.

    Example:
        ```python
        # Ensure user is both active and staff
        @requires_permissions(IsActive() & IsStaff())
        def active_staff_only(request):
            ...
        ```
    """

    def resolve(self, user: AbstractUser) -> bool:
        """Check if the user account is active.

        Args:
            user: The Django user to check

        Returns:
            True if the user account is active, False otherwise
        """
        return user.is_active


__all__ = ["P", "IsAdmin", "IsSuperuser", "IsStaff", "IsActive", "requires_permissions"]
