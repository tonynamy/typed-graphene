import dataclasses
from functools import cache
from inspect import isclass
from types import NoneType, UnionType
from typing import Any, NotRequired, Optional, Type, Union, cast, get_args, get_origin

import graphene
from graphene.types.unmountedtype import UnmountedType

from .transformers.register import TRANSFORMERS
from .transformers import DEFAULT_TRANSFORMERS


def get_nested_type(T: Type):
    """
    Returns the inner type of a nested type.
    """
    return get_args(T)[0]


def get_type_and_required(T: Type) -> tuple[Type, bool]:
    """
    Returns the inner type of a nested type and whether it is required.
    """

    required = True

    # NOTE
    # Union: `typing.Union[str, None]`
    # UnionType: `str | None`
    if get_origin(T) == Union or get_origin(T) == UnionType:
        inner_types = cast(tuple[Type], T.__args__)

        T = Union[tuple(filter(lambda t: t != NoneType, inner_types))]
        required = NoneType not in inner_types

    # NOTE
    # NotRequired: `NotRequired[str]`
    # Optional: `typing.Optional[str]`
    elif get_origin(T) == NotRequired or get_origin(T) == Optional:
        T = T.__args__[0]
        required = False

    return T, required


@cache
def python_type_to_graphene_type_and_kwargs(T: Type) -> tuple[Type, dict[str, Any]]:
    """
    Convert a python type to a graphene type and kwargs.
    This function is recursive.
    Caution: This function is cached, so it always returns the same graphene type for the same python type.
    DO NOT mutate the returned value.
    """

    graphene_type = None
    kwargs = {}

    T, kwargs["required"] = get_type_and_required(T)

    # NOTE: typing.TypedDict
    # See https://github.com/pydantic/pydantic/issues/1430#issuecomment-725633396
    if getattr(T.__class__, "__name__", None) == "_TypedDictMeta":
        type_dict = {}

        for name, item_type in T.__annotations__.items():
            type_dict[name] = python_type_to_graphene_instance(item_type)

        graphene_type = type(T.__name__, (graphene.InputObjectType,), type_dict)

    # NOTE: dataclasses.dataclass
    elif dataclasses.is_dataclass(T):
        type_dict = {}

        for field in dataclasses.fields(T):
            name, item_type = field.name, field.type
            inner_type, inner_kwargs = python_type_to_graphene_type_and_kwargs(
                item_type
            )

            # NOTE: String(), Int(), etc.
            if issubclass(inner_type, UnmountedType):
                type_dict[name] = inner_type(**inner_kwargs)

            # NOTE: Field(XXXObjectType)
            else:
                type_dict[name] = graphene.Field(inner_type, **inner_kwargs)

        graphene_type = type(T.__name__, (graphene.ObjectType,), type_dict)

    elif get_origin(T) == list:
        graphene_type = graphene.List
        inner_type = get_nested_type(T)

        graphene_inner_type, inner_kwargs = python_type_to_graphene_type_and_kwargs(
            inner_type  # type: ignore[arg-type]
        )

        if inner_kwargs.get("required", True):
            graphene_inner_type = graphene.NonNull(graphene_inner_type)

        kwargs["of_type"] = graphene_inner_type  # type: ignore[assignment]

    else:
        try:
            graphene_type = next(
                transformer.transform_type(T)
                for transformer in TRANSFORMERS + DEFAULT_TRANSFORMERS
                if transformer.check_type(T)
            )

        except StopIteration:
            if isclass(T) and (
                issubclass(T, UnmountedType)
                or issubclass(T, graphene.ObjectType)
                or issubclass(T, graphene.Interface)
            ):
                graphene_type = T

    if not graphene_type:
        raise NotImplementedError(f"{str(T)} is not implemented")

    return graphene_type, kwargs


def python_type_to_graphene_instance(T: Type):
    T, kwargs = python_type_to_graphene_type_and_kwargs(T)
    return T(**kwargs)
