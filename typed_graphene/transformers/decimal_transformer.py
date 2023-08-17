from graphene import Decimal as GrapheneDecimal

from .base_transformer import BaseTransformer
from .register import register
from decimal import Decimal


@register
class DeicmalTransformer(BaseTransformer[Decimal, GrapheneDecimal]):
    python_type = Decimal
    graphene_type = GrapheneDecimal
