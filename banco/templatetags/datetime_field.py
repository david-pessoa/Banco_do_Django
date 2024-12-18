from django import template
from django.utils.timezone import localtime

register = template.Library()
@register.filter(name="format_datetime")
def format_datetime(value):
    fuso = localtime(value)
    return fuso.strftime("%d/%m/%Y  %H:%M")