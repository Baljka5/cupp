# your_app/templatetags/event_tags.py

from django import template
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

register = template.Library()


@register.simple_tag(takes_context=True)
def is_in_event_group(context):
    request = context['request']
    return request.user.groups.filter(name='Event').exists() or request.user.is_superuser


@register.simple_tag(takes_context=True)
def is_in_store_planner_group(context):
    request = context['request']
    return request.user.groups.filter(name='Store Planner').exists() or request.user.is_superuser


@register.simple_tag(takes_context=True)
def is_in_license_group(context):
    request = context['request']
    return request.user.groups.filter(name='license').exists() or request.user.is_superuser


@login_required
def custom_login_redirect(request):
    if request.user.is_superuser:
        return redirect('/map/')  # Redirect URL for superusers
    elif request.user.groups.filter(name='Event').exists():
        return redirect('/event-index/')  # Redirect URL for users in Event group
    else:
        return redirect('/default-redirect/')