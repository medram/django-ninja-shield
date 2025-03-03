from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


class BaseOperation(abc.ABC):
    def __init__(self, perm1: BaseOperation, perm2: BaseOperation):
        self._perm1 = perm1
        self._perm2 = perm2

    @abc.abstractmethod
    def resolve(self, user: AbstractUser) -> bool: ...

    def __and__(self, other: BaseOperation):
        return AND(self, other)

    def __or__(self, other: BaseOperation):
        return OR(self, other)

    def __invert__(self):
        return NOT(self)


class P(BaseOperation):
    """P stand for Permission"""

    def __init__(self, permission: str):
        self._permission = permission

    def resolve(self, user: AbstractUser) -> bool:
        return user.has_perm(self._permission)


class AtomicOperation(BaseOperation):
    def __init__(self) -> None: ...


#### Operations ####
class AND(BaseOperation):
    def resolve(self, user: AbstractUser) -> bool:
        return self._perm1.resolve(user) and self._perm2.resolve(user)


class OR(BaseOperation):
    def resolve(self, user: AbstractUser) -> bool:
        return self._perm1.resolve(user) or self._perm2.resolve(user)


class NOT(BaseOperation):
    def __init__(self, op: BaseOperation):
        self._op = op

    def resolve(self, user: AbstractUser) -> bool:
        return not self._op.resolve(user)


__all__ = ["P", "BaseOperation", "AtomicOperation"]
