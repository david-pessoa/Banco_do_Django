from django import template
from datetime import datetime

register = template.Library()
@register.filter(name="format_datetime")
def format_datetime(value):
    return value.strftime("%d/%m/%Y  %H:%M")