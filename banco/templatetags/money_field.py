from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name="format_money")
def format_money(value):
    if value is None:
        return "0,00"
    
    return "{:,.2f}".format(Decimal(value)).replace(".", "#").replace(",", ".").replace("#", ",")
    