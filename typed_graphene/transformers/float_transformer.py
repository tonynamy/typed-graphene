from graphene import Float

from .base_transformer import BaseTransformer
from .register import register


@register
class FloatTransformer(BaseTransformer[float, Float]):
    python_type = float
    graphene_type = Float
