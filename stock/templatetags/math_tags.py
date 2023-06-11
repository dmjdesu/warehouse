from django import template

register = template.Library()

@register.simple_tag
def set(value):
    return value