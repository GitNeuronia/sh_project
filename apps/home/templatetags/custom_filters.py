from django import template
from decimal import Decimal
import json

import locale

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
    return json.dumps(value)@register.filter

@register.filter
def custom_number_format(value):
    # Establecer la localización para usar separadores de miles según sea necesario
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

    # Si value es None o no se puede convertir a float, se trata como 0
    try:
        valor = float(value)
    except (TypeError, ValueError):
        valor = 0

    # Comprobamos si el número es entero comparándolo con su versión entera
    if valor == int(valor):
        # Formatear como número entero (sin decimales)
        formatted_number = locale.format_string('%d', int(valor), grouping=True)
    else:
        # Formatear como número con decimales (hasta 3)
        formatted_number = locale.format_string('%.3f', valor, grouping=True)
        
        # Eliminar ceros innecesarios al final
        while formatted_number.endswith('0'):
            formatted_number = formatted_number[:-1]
        if formatted_number.endswith(','):
            formatted_number = formatted_number[:-1]

    return formatted_number
