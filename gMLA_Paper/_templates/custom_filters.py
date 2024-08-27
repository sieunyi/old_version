# In a file like myapp/templatetags/custom_filters.py

from django import template
import re

register = template.Library()

@register.filter
def format_earnings(value):
    # Remove any non-digit characters except for the decimal point and minus sign
    cleaned = re.sub(r'[^\d.-]', '', str(value))
    # Convert to float and format
    return f'${float(cleaned):.2f}'


def dict_lookup(obj, key):
    return getattr(obj, key)