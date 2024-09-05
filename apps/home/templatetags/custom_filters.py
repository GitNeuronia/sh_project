from django import template
from decimal import Decimal
register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter(name='div')
def div(value, arg):
    try:
        return Decimal(value) / Decimal(arg)
    except (ValueError, ZeroDivisionError):
        return None