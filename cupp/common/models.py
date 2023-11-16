from django.db import models as m
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Model to store the list of logged in users
class LoggedInUser(m.Model):
    user = m.OneToOneField(User, related_name='logged_in_user', on_delete=m.CASCADE)
    # Session keys are 32 characters long
    session_key = m.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
