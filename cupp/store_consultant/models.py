import os
import uuid

from django.db import models as m
from django.contrib.auth.models import User


class StoreConsultant(m.Model):
    store_id = m.IntegerField('Store ID', blank=True, null=True, default=0)
    team_mgr = m.CharField('Team manager name', blank=True, null=True, max_length=50)
    sc_name = m.CharField('Store consultant name', blank=True, null=True, max_length=50)
    tt_type = m.CharField('Working timetable', blank=True, null=True, max_length=50)
    wday_hours = m.TimeField('Timetable', blank=True, null=True)
    wend_hours = m.TimeField('Timetable', blank=True, null=True)
    atm = m.IntegerField('ATM number', blank=True, null=True, default=0)
    chest_frz_ru = m.IntegerField('Horizontal freezer /Russian, Mongolia/', blank=True, null=True, default=0)
    chest_frz_kr = m.IntegerField('Horizontal freezer /Korea/', blank=True, null=True, default=0)
    up_frz_kr = m.IntegerField('Vertical freezer /Korea', blank=True, null=True, default=0)
    ba_rob_frz = m.IntegerField('Baskin robbins freezer', blank=True, null=True, default=0)
    up_frz_suu = m.IntegerField('Horizontal milk freezer', blank=True, null=True, default=0)
    up_frz_ice = m.IntegerField('Horizontal icemark freezer', blank=True, null=True)
    storabox = m.BooleanField('Stora Box', blank=True, null=True)
    Umoney = m.BooleanField('Bus card stadium or not', blank=True, null=True)
    alc_reason = m.TextField('Reason for not having alcohol license', blank=True, null=True)
    ciga_reason = m.TextField('Reason for not having cigar license', blank=True, null=True)
    reason_not_24 = m.TextField('Reason for not having 24 hour working', blank=True, null=True)
    close_date = m.DateField('Closing date', blank=True, null=True)
    close_reason = m.TextField('Reason for closing store', blank=True, null=True)
    near_store = m.IntegerField('Number of the store within 500 meters', blank=True, null=True, default=0)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='store_consultant_created',
                              on_delete=m.PROTECT, null=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='store_consultant_modified',
                               on_delete=m.PROTECT, null=True)

    def __str__(self):
        return self.store_id

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(StoreConsultant, self).save(*args, **kwargs)

    class Meta:
        db_table = 'store_consultant'
        verbose_name = 'Store Consultant'