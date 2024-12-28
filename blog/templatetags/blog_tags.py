from django import template
import math
from django.db.models import Count
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='reading_time')
def reading_time(text):
    """
    Calculate reading time in minutes
    Assumes average reading speed of 200 words per minute
    """
    if not text:
        return 0
    words = len(str(text).split())
    return max(1, math.ceil(words / 200))
