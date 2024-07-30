from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.simple_tag(takes_context=True)
def is_in_store_planner_group(context):
    request = context['request']
    return request.user.groups.filter(name='Store planner').exists() or request.user.is_superuser
