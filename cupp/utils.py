from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


def create_user(username, first_name='', last_name='', email='', group=None, password=None,
                is_active=True, is_superuser=False):
    user = User.objects.create(
        username=username,
        password=make_password(password if password else get_random_string(length=6, allowed_chars='0123456789')),
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=is_active,
        is_superuser=is_superuser,
        is_staff=is_superuser
    )

    if group:
        user.groups.add(Group.objects.get_or_create(name=group)[0])

    return user


def dict_to_obj(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset

    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, dict_to_obj(j))
        elif isinstance(j, seqs):
            setattr(top, i, type(j)(dict_to_obj(sj) if isinstance(sj, dict) else sj for sj in j))
        elif isinstance(j, str):
            setattr(top, i, j.strip())
        else:
            setattr(top, i, j)

    return top


def is_mobile(mobile):
    return mobile.isdigit() and len(mobile) == 8 and mobile[:2] in settings.OPERATOR_PREFIXES


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
