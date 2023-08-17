from graphene import Boolean

from .base_transformer import BaseTransformer
from .register import register


@register
class BoolTransformer(BaseTransformer[bool, Boolean]):
    python_type = bool
    graphene_type = Boolean
