from types import UnionType
from typing import Any, Type, TypeAlias

from graphene import Field

from .utils import (
    python_type_to_graphene_instance,
    python_type_to_graphene_type_and_kwargs,
)

__all__ = [
    "TypedField",
]


class TypedField(Field):
    """
    Wraps graphene.Field to support type-hinted arguments
    Doesn't support `required` argument, use `None` and union instead.

    .. code:: python
        from typed_graphene import TypedField

        class Person(ObjectType):
            name = TypedField(str)  # Same with `graphene.Field(String, required=True)`
    """

    def __init__(  # type: ignore[no-untyped-def]
        self,
        T: Type | UnionType | TypeAlias,
        args=None,
        resolver=None,
        source=None,
        deprecation_reason=None,
        name=None,
        description=None,
        _creation_counter=None,
        default_value=None,
        **extra_args: Any
    ) -> None:
        T, kwargs = python_type_to_graphene_type_and_kwargs(T)  # type: ignore[arg-type]
        kwargs = kwargs.copy()
        required = kwargs.pop("required", True)

        if "required" in extra_args:
            raise AssertionError(
                "Cannot specify required for TypedField. Concat the type with `None` instead."
            )

        for k, v in extra_args.items():
            extra_args[k] = python_type_to_graphene_instance(v)

        super().__init__(
            # NOTE: if T is list, kwargs will be `of_type` argument
            T(**kwargs) if bool(kwargs) else T,
            args,
            resolver,
            source,
            deprecation_reason,
            name,
            description,
            required,
            _creation_counter,
            default_value,
            **extra_args
        )
