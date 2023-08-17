from functools import cache
from typing import Any, Generic, TypeGuard, TypeVar
from graphene import Scalar

_T = TypeVar("_T", bound=object)
_S = TypeVar("_S", bound=Scalar)


class BaseTransformer(Generic[_T, _S]):
    python_type: type[_T]
    graphene_type: type[_S]

    @classmethod
    @cache
    def check_type(cls, T: type[Any]) -> TypeGuard[type[_T]]:
        """Check if the type is the guarded type."""
        return T == cls.python_type

    @classmethod
    @cache
    def transform_type(cls, T: type[_T]) -> type[_S]:
        """Transform the type into the graphene type."""
        return cls.graphene_type
