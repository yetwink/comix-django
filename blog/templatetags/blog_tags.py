from blog.models import Genre
from django import template

register = template.Library()

@register.simple_tag()
def get_genres():
    return Genre.objects.all()