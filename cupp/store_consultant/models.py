import os
import uuid

from django.db import models as m
from django.contrib.auth.models import User


class StoreConsultant(m.Model):
    store_id = m.CharField('Store ID', blank=True, null=True, max_length=5)
    store_name = m.CharField('Store Name', blank=True, null=True, max_length=50)
    team_mgr = m.CharField('Team manager name', blank=True, null=True, max_length=50)
    sc_name = m.CharField('Store consultant name', blank=True, null=True, max_length=50)
    sm_num = m.IntegerField('Дэлгүүрийн менежерийн тоо', blank=True, null=True)
    am_num = m.IntegerField('Дэлгүүрийн туслах менежерийн тоо', blank=True, null=True)
    tt_type = m.CharField('Working timetable', blank=True, null=True, max_length=50)
    wday_hours = m.CharField('Timetable', blank=True, null=True, max_length=50)
    wend_hours = m.CharField('Timetable', blank=True, null=True, max_length=50)
    atm = m.IntegerField('ATM number', blank=True, null=True, default=0)
    chest_frz_ru = m.IntegerField('Horizontal freezer /Russian, Mongolia/', blank=True, null=True, default=0)
    chest_frz_kr = m.IntegerField('Horizontal freezer /Korea/', blank=True, null=True, default=0)
    up_frz_kr = m.IntegerField('Vertical freezer /Korea', blank=True, null=True, default=0)
    ba_rob_frz = m.IntegerField('Baskin robbins freezer', blank=True, null=True, default=0)
    up_frz_suu = m.IntegerField('Horizontal milk freezer', blank=True, null=True, default=0)
    up_frz_ice = m.IntegerField('Horizontal icemark freezer', blank=True, null=True)
    ser_storabox = m.BooleanField('Stora Box', blank=True, null=True)
    ser_Umoney = m.BooleanField('Автобусны карт цэнэглэгчтэй эсэх', blank=True, null=True)
    ser_pow_bank = m.BooleanField('Зөөврийн цэнэглэгч түрээс', blank=True, null=True)
    ser_lottery = m.BooleanField('Сугалаа', blank=True, null=True)
    ser_delivery = m.BooleanField('Хүргэлт', blank=True, null=True)
    ser_print = m.BooleanField('Хэвлэл', blank=True, null=True)
    ser_ticket = m.BooleanField('Тасалбар', blank=True, null=True)
    alc_reason = m.TextField('Reason for not having alcohol license', blank=True, null=True)
    ciga_reason = m.TextField('Reason for not having cigar license', blank=True, null=True)
    reason_not_24 = m.TextField('Reason for not having 24 hour working', blank=True, null=True)
    close_date = m.DateField('Closing date', blank=True, null=True)
    close_reason = m.TextField('Reason for closing store', blank=True, null=True)
    near_gs = m.CharField('GS detail status', blank=True, null=True, max_length=100)
    sm_name = m.CharField('Store manager name', blank=True, null=True, max_length=50)
    sm_phone = m.IntegerField('Store manager phone', blank=True, null=True, default=0)
    prc_grade = m.CharField('Pricing policy', blank=True, null=True, max_length=50)
    tv_screen = m.IntegerField('Tv screen', blank=True, null=True)
    toilet_tp = m.BooleanField('00-н төрөл (Өөрийн, нийтийн)', blank=True, null=True)
    walkin_chiller = m.IntegerField('Уух ус ундааны босоо хөргүүрийн хаалганы тоо', blank=True, null=True, default=0)
    lunch_case_L8 = m.IntegerField('Хоолны хөргүүрийн тоо ', blank=True, null=True, default=0)
    created_date = m.DateTimeField('Created date', auto_now_add=True, null=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True, null=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='store_consultant_created',
                              on_delete=m.PROTECT, null=True, blank=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='store_consultant_modified',
                               on_delete=m.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.store_id

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(StoreConsultant, self).save(*args, **kwargs)

    class Meta:
        db_table = 'store_consultant'
        verbose_name = 'Store Consultant'


class Area(m.Model):
    team_no = m.CharField('Area No', max_length=10, blank=True, null=True)
    team_man_name = m.CharField('Area manager name', max_length=50, blank=True, null=True)
    team_man_surname = m.CharField('Area manager surname', max_length=50, blank=True, null=True)
    team_man_email = m.EmailField('Area manager email address', blank=True, null=True)
    team_man_phone = m.IntegerField('Area manager phone number', blank=True, null=True, default=0)
    team_man_sex = m.BooleanField('Area manager gender', blank=True, null=True)
    team_man_birthdt = m.DateField('Area manager birthday', blank=True, null=True)
    team_man_rel_status = m.BooleanField('Area manager marital status', blank=True, null=True)
    team_man_child = m.IntegerField('Area manager number of children', blank=True, null=True, default=0)
    team_man_Addr1 = m.CharField('Living city', blank=True, null=True, max_length=50)
    team_man_Addr2 = m.CharField('Living district', blank=True, null=True, max_length=50)
    team_man_Addr3 = m.CharField('Living khoroo', blank=True, null=True, max_length=50)
    team_man_Addr4 = m.CharField('Address detail', blank=True, null=True, max_length=50)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='area_manager_created', on_delete=m.PROTECT,
                              null=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='area_manager_modified',
                               on_delete=m.PROTECT,
                               null=True)

    def __str__(self):
        return '%s - %s' % (self.team_no, self.team_man_name)

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(Area, self).save(*args, **kwargs)

    class Meta:
        db_table = 'area_manager'
        verbose_name = 'Area Manger'


class Consultants(m.Model):
    sc_name = m.CharField('Store name of consultants', max_length=50, blank=True, null=True)
    sc_surname = m.CharField('Surname of store consultants', max_length=50, blank=True, null=True)
    sc_email = m.EmailField('Email address of store consultants', blank=True, null=True)
    sc_phone = m.IntegerField('Phone number of store consultants', blank=True, null=True)
    sc_sex = m.BooleanField('Gender of store consultant', blank=True, null=True)
    sc_birthdt = m.DateField('Birth date of store consultant', blank=True, null=True)
    sc_rel_status = m.BooleanField('Relation status of store consultant', blank=True, null=True)
    sc_child = m.IntegerField('Child number of store consultant', blank=True, null=True)
    sc_Addr1 = m.CharField('Living city', blank=True, null=True, max_length=50)
    sc_Addr2 = m.CharField('Living district', blank=True, null=True, max_length=50)
    sc_Addr3 = m.CharField('Living khoroo', blank=True, null=True, max_length=50)
    sc_Addr4 = m.CharField('Detail address', blank=True, null=True, max_length=50)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='sc_created', on_delete=m.PROTECT,
                              null=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='sc_modified',
                               on_delete=m.PROTECT,
                               null=True)

    def __str__(self):
        return self.sc_name

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(Consultants, self).save(*args, **kwargs)

    class Meta:
        db_table = 'consultant'
        verbose_name = 'Consultant'


class Allocation(m.Model):
    consultant = m.ForeignKey(Consultants, on_delete=m.CASCADE, null=True, blank=True)
    area = m.ForeignKey(Area, on_delete=m.SET_NULL, null=True, blank=True)
    year = m.CharField('Year', max_length=4, blank=True, null=True)
    month = m.CharField('Month', max_length=12, blank=True, null=True)
    team_no = m.CharField('Team No', max_length=10, blank=True, null=True)
    store_cons = m.CharField('Store Consultant', max_length=50, blank=True, null=True)
    storeID = m.CharField('Store ID', max_length=5, blank=True, null=True)
    store_name = m.CharField('Store Name', max_length=50, blank=True, null=True)
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='allocation_created', on_delete=m.PROTECT,
                              null=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='allocation_modified',
                               on_delete=m.PROTECT,
                               null=True)

    def __str__(self):
        return self.team_no

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(Allocation, self).save(*args, **kwargs)

    class Meta:
        db_table = 'allocation'
        verbose_name = 'Allocation'
