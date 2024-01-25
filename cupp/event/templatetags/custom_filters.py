# custom_filters.py
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def user_belongs_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        print(group)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False
