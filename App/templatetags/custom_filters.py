from django import template

register = template.Library()


@register.filter(name="split")
def split(val, sep):
    return val.split(sep)[0] + ' ' + val.split(sep)[1]