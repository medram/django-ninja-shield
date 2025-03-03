from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING

from django.http import HttpRequest, JsonResponse

from .base import P

if TYPE_CHECKING:
    from .base import BaseOperation


def requires_permissions(permission_operation: BaseOperation | str):
    """Decorator to protect Django views with permission checks.

    This decorator can work with both string-based Django permissions and
    custom BaseOperation permission objects. If a string is provided, it's
    automatically converted to a P() permission object.

    Args:
        permission_operation: Either a BaseOperation instance for complex
            permission checks, or a string for simple Django model permissions

    Returns:
        A decorator function that wraps the view

    Example:
        ```python
        # Using with Django's built-in permissions
        @requires_permissions('blog.add_post')
        def create_post(request):
            ...

        # Using with custom permission operations
        @requires_permissions(IsAdmin() | IsStaff())
        def admin_dashboard(request):
            ...

        # Combining multiple permissions
        @requires_permissions(IsActive() & (IsAdmin() | IsStaff()))
        def protected_view(request):
            ...
        ```

    Note:
        If permission is denied, returns a 403 Forbidden response with a
        JSON message {"detail": "Permission denied"}
    """
    if isinstance(permission_operation, str):
        permission_operation = P(permission_operation)

    def decorator(fn: Callable) -> Callable:
        """Create the actual decorator with the configured permission check.

        Args:
            fn: The view function to protect

        Returns:
            The wrapped view function with permission checking
        """

        @wraps(fn)
        def wrapped(request: HttpRequest, *args, **kwargs):
            """Check permissions before executing the view.

            Args:
                request: The Django HTTP request
                *args: Positional arguments to pass to the view
                **kwargs: Keyword arguments to pass to the view

            Returns:
                The view's response if permitted, else a 403 JSON response
            """
            if request.user and permission_operation.resolve(request.user):  # type: ignore
                return fn(request, *args, **kwargs)

            return JsonResponse({"detail": "Permission denied"}, status=403)

        return wrapped

    return decorator


__all__ = ["requires_permissions"]
