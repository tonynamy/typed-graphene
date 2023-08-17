from typing import TypeVar

from .base_transformer import BaseTransformer

_T = TypeVar("_T", bound=BaseTransformer)

TRANSFORMERS: list[type[_T]] = []


def register(klass: type[_T]) -> type[_T]:
    """
    Mark transformer to be registered.
    """
    TRANSFORMERS.append(klass)
    return klass
