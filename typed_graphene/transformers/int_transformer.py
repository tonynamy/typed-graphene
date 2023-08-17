from graphene import Int

from .base_transformer import BaseTransformer
from .register import register


@register
class IntTransformer(BaseTransformer[int, Int]):
    python_type = int
    graphene_type = Int
