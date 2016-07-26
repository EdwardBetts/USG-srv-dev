from django import template

register = template.Library()

def hash(h, key):
    return h.get(key)

register.filter('hash', hash)
