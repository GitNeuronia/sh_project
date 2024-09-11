from django import template
from decimal import Decimal
import json

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
    
@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter
def get_item(list_data, index):
    try:
        return list_data[int(index)]
    except:
        return None
    
@register.filter
def make_list(value):
    return list(value)

@register.filter(name='json_encode')
def json_encode(value):
    return json.dumps(value)