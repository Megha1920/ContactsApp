# contacts/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def format_phone_numbers(value):
    # Assuming value is a comma-separated string of phone numbers
    phone_numbers = value.split(',')
    return ', '.join([num.strip() for num in phone_numbers])
