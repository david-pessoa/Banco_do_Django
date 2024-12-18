from django import template

register = template.Library()
@register.filter(name="format_chave_pix")
def format_chave_pix(value):
    hidden_len = len(value) - 5
    show_value = value[:5]
    return show_value + hidden_len * "*"
