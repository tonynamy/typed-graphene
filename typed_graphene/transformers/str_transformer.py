from graphene import String

from .base_transformer import BaseTransformer
from .register import register


@register
class StrTransformer(BaseTransformer[str, String]):
    python_type = str
    graphene_type = String
