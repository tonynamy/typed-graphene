from datetime import datetime

from graphene import DateTime

from .base_transformer import BaseTransformer
from .register import register


@register
class DateTimeTransformer(BaseTransformer[datetime, DateTime]):
    python_type = datetime
    graphene_type = DateTime
