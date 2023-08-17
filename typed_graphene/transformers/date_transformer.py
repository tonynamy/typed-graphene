from datetime import date

from graphene import Date

from .base_transformer import BaseTransformer
from .register import register


@register
class DateTransformer(BaseTransformer[date, Date]):
    python_type = date
    graphene_type = Date
