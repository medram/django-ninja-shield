from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING

from django.http import HttpRequest, JsonResponse

from .base import P

if TYPE_CHECKING:
    from .base import BaseOperation


def requires_permissions(permission_operation: BaseOperation | str):
    if isinstance(permission_operation, str):
        permission_operation = P(permission_operation)

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapped(request: HttpRequest, *args, **kwargs):
            if request.user and permission_operation.resolve(request.user):  # type: ignore
                return fn(request, *args, **kwargs)

            return JsonResponse({"detail": "Permission denied"}, status=403)

        return wrapped

    return decorator


__all__ = ["requires_permissions"]
