import os
import uuid

from django.db import models as m
from django.contrib.auth.models import User
from django.conf import settings
from uuid import uuid4

from cupp.constants import CHOICES_POINT_TYPE, CHOICES_POINT_GRADE


# from cupp.choices import get_point_type_choices


def upload_file(instance, filename):
    return 'point/%s%s' % (str(uuid.uuid4())[:12], os.path.splitext(filename)[1])


def icon_file(instance, filename):
    return 'static/%s%s' % (str(uuid.uuid4())[:12], os.path.splitext(filename)[1])


class City(m.Model):
    city_code = m.IntegerField('City and aimag code', blank=False, null=True, default=0)
    city_name = m.CharField('City and aimag name', blank=False, default='', max_length=50, unique=True)

    def __str__(self):
        return self.city_name

    class Meta:
        db_table = 'cupp_city'
        verbose_name = 'City'


class District(m.Model):
    district_name = m.CharField('District and sum name', blank=False, default='', max_length=50, unique=True)
    city = m.ForeignKey(City, on_delete=m.CASCADE, related_name='districts')

    def __str__(self):
        return self.district_name

    class Meta:
        db_table = 'cupp_district'
        verbose_name = 'District'


class Type(m.Model):
    type_name = m.CharField('Type name', blank=False, default='', max_length=50, unique=True)
    type_cd = m.CharField('Type code', blank=False, default='', max_length=50, unique=True)
    icon = m.FileField(upload_to='images/ui')  # Temporarily store files

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'cupp_type'
        verbose_name = 'Type'


# def get_type_choices():
#     return [(type.type_cd, type.type_name) for type in Type.objects.all()]

class Point(m.Model):
    created_date = m.DateTimeField('Created date', auto_now_add=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True)

    created_by = m.ForeignKey(User, verbose_name='Creadted by', related_name='points', on_delete=m.PROTECT)

    # type = m.CharField('Type', max_length=10, choices=get_type_choices())
    store_id = m.IntegerField('Store ID', blank=True, null=True, default=0)
    store_name = m.CharField('Store name', blank=True, null=True, max_length=500)
    type = m.CharField('Type', max_length=10, choices=CHOICES_POINT_TYPE)
    lat = m.CharField('Latitude', max_length=50, default='47.9116')
    lon = m.CharField('Longitude', max_length=50, default='106.9057')

    grade = m.CharField('Location grade', max_length=10, choices=CHOICES_POINT_GRADE, blank=True, null=True,
                        default='A')
    size = m.IntegerField('Size', blank=True, null=True, default=0)
    address = m.CharField('Address', blank=False, default='', max_length=200)

    owner_name = m.CharField('Landlord name', max_length=50, blank=True, null=True)
    owner_phone = m.CharField('Landlord phone', max_length=50, blank=True, null=True)
    owner_email = m.CharField('Landlord email', max_length=50, blank=True, null=True)

    base_rent_rate = m.IntegerField('Base rent', blank=True, null=True, default=0)
    max_rent_rate = m.IntegerField('Maximum rent', blank=True, null=True, default=0)
    turnover_rent_percent = m.IntegerField('Turnover rent percentage', blank=True, null=True, default=0)
    radius = m.IntegerField('Radius by meter /limit 1km/', blank=True, null=True, default=0)
    isr_file = m.FileField('ISR excel file', upload_to=upload_file, blank=True, null=True)
    pl_file = m.FileField('P&L excel file', upload_to=upload_file, blank=True, null=True)

    proposed_layout = m.FileField('Proposed layout', upload_to=upload_file, blank=True, null=True)

    availability = m.BooleanField('Availability', blank=True, null=True)
    available_date = m.DateField('Available date', blank=True, null=True)

    deposit = m.IntegerField('Deposit', blank=True, null=True, default=0)
    bep = m.IntegerField('Breakeven point', blank=True, null=True, default=0)
    expected_sales = m.IntegerField('Expected daily sales', blank=True, null=True, default=0)
    passers = m.IntegerField('Average passers an hour', blank=True, null=True, default=0)
    hh = m.IntegerField('Households in the direct area', blank=True, null=True, default=0)
    office = m.IntegerField('Office people in the direct area', blank=True, null=True, default=0)
    students = m.IntegerField('School/University students in the direct area', blank=True, null=True, default=0)
    # created_by_id = m.ForeignKey(User, verbose_name='Created by', related_name='store_planning_created',
    #                           on_delete=m.PROTECT, null=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='points_modified',
                               on_delete=m.PROTECT, null=True)

    def __str__(self):
        return '%s - %s' % (self.get_type_display(), self.address)

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(Point, self).save(*args, **kwargs)

    class Meta:
        db_table = 'cupp_point'
        verbose_name = 'Point'


class PointPhoto(m.Model):
    point = m.ForeignKey(Point, related_name='photos', on_delete=m.CASCADE)
    photo = m.ImageField(upload_to=upload_file)

    class Meta:
        db_table = 'cupp_point_photo'
        verbose_name = 'Point Photo'
