import os
import uuid

from django.db import models as m
from django.contrib.auth.models import User
from django.conf import settings
from uuid import uuid4


class ActionOwner(m.Model):
    own_id = m.CharField(max_length=100, primary_key=True)
    own_pos = m.CharField(max_length=255)
    own_dep = m.CharField(max_length=255)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    created_by = m.ForeignKey(User, verbose_name='Creadted by', related_name='action_owners', on_delete=m.PROTECT)

    def __str__(self):
        return self.own_id

    class Meta:
        db_table = 'action_owners'
        verbose_name = 'Action owners'


class StoreDailyLog(m.Model):
    date = m.DateField()
    store_no = m.CharField(max_length=100)
    store_name = m.CharField(max_length=255)
    activ_desc = m.TextField()
    activ_cat = m.ForeignKey('ActionCategory', on_delete=m.CASCADE)
    resp_action = m.TextField()
    action_owner = m.ForeignKey('ActionOwner', on_delete=m.CASCADE)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    created_by = m.ForeignKey(User, verbose_name='Creadted by', related_name='store_daily_logs', on_delete=m.PROTECT,
                              null=True)

    def __str__(self):
        return f"{self.store_name} - {self.date}"

    class Meta:
        db_table = 'store_daily_log'
        verbose_name = 'Store Daily Logs'

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = self.created_by.date_joined  # or any other date field from the User model
        super().save(*args, **kwargs)


class ActionCategory(m.Model):
    activ_id = m.CharField(max_length=100, primary_key=True)
    activ_cat = m.CharField(max_length=255)
    activ_desc = m.TextField()
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    created_by = m.ForeignKey(User, verbose_name='Creadted by', related_name='action_categories', on_delete=m.PROTECT)

    def __str__(self):
        return self.activ_cat

    class Meta:
        db_table = 'action_category'
        verbose_name = 'Action Category'
