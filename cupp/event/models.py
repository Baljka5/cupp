import os
import uuid

from django.db import models as m
from django.contrib.auth.models import User
from django.conf import settings
from uuid import uuid4
from django.core.validators import RegexValidator


class ActionOwner(m.Model):
    own_id = m.CharField(max_length=100, primary_key=True)
    own_pos = m.CharField(max_length=255)
    own_dep = m.CharField(max_length=255)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='action_owners_created',
                              on_delete=m.PROTECT, null=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='action_owners_modified',
                               on_delete=m.PROTECT, null=True)

    def __str__(self):
        return self.own_dep

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(ActionOwner, self).save(*args, **kwargs)

    class Meta:
        db_table = 'action_owners'
        verbose_name = 'Action owners'


class StoreDailyLog(m.Model):
    five_digit_validator = RegexValidator(r'^\d{5}$', 'Store number must be a 5-digit number')

    date = m.DateField()
    store_no = m.CharField(max_length=5, validators=[five_digit_validator])
    store_name = m.CharField(max_length=255)
    activ_desc = m.TextField()
    activ_cat = m.ForeignKey('ActionCategory', on_delete=m.CASCADE)
    resp_action = m.TextField(null=True, blank=True)
    action_owner = m.ForeignKey('ActionOwner', on_delete=m.CASCADE)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='store_daily_logs_created',
                              on_delete=m.PROTECT, null=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='store_daily_logs_modified',
                               on_delete=m.PROTECT, null=True)
    consequences = m.BooleanField('Consequences of events', null=True, blank=True)

    def __str__(self):
        return self.action_owner.own_dep

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(StoreDailyLog, self).save(*args, **kwargs)

    class Meta:
        db_table = 'store_daily_log'
        verbose_name = 'Store Daily Logs'


class ActionCategory(m.Model):
    activ_id = m.CharField(max_length=100, primary_key=True)
    activ_cat = m.CharField(max_length=255)
    activ_desc = m.TextField()
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='action_categories_created',
                              on_delete=m.PROTECT, null=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='action_categories_modified',
                               on_delete=m.PROTECT, null=True)

    def __str__(self):
        return self.activ_cat

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(ActionCategory, self).save(*args, **kwargs)

    class Meta:
        db_table = 'action_category'
        verbose_name = 'Action Category'
