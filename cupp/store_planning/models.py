# import os
# import uuid
#
# from django.db import models as m
# from django.contrib.auth.models import User
# from cupp.point.models import City, District, upload_file
#
# from cupp.constants import CHOICES_POINT_TYPE, CHOICES_POINT_GRADE
#
#
# class StorePlanning(m.Model):
#     store_id = m.IntegerField('Store ID', blank=True, null=True, default=0)
#     store_name = m.CharField('Store name', blank=True, null=True, max_length=500)
#     lat = m.CharField('Latitude', max_length=50, default='47.9116')
#     lon = m.CharField('Longitude', max_length=50, default='106.9057')
#     grade = m.CharField('Location grade', max_length=10, choices=CHOICES_POINT_GRADE, blank=True, null=True,
#                         default='A')
#     size = m.IntegerField('Size', blank=True, null=True, default=0)
#     owner_name = m.CharField('Landlord name', max_length=50, blank=True, null=True)
#     owner_phone = m.CharField('Landlord phone', max_length=50, blank=True, null=True)
#     owner_email = m.CharField('Landlord email', max_length=50, blank=True, null=True)
#     base_rent_rate = m.IntegerField('Base rent', blank=True, null=True, default=0)
#     proposed_layout = m.FileField('Proposed layout', upload_to=upload_file, blank=True, null=True)
#     availability = m.BooleanField('Availability', blank=True, null=True)
#     deposit = m.IntegerField('Deposit', blank=True, null=True, default=0)
#     bep = m.IntegerField('Breakeven point', blank=True, null=True, default=0)
#     expected_sales = m.IntegerField('Expected daily sales', blank=True, null=True, default=0)
#     passers = m.IntegerField('Average passers an hour', blank=True, null=True, default=0)
#     hh = m.IntegerField('Households in the direct area', blank=True, null=True, default=0)
#     office = m.IntegerField('Office people in the direct area', blank=True, null=True, default=0)
#     students = m.IntegerField('School/University students in the direct area', blank=True, null=True, default=0)
#     available_date = m.DateField('Available date', blank=True, null=True)
#     isr_file = m.FileField('ISR excel file', upload_to=upload_file, blank=True, null=True)
#     max_rent_rate = m.IntegerField('Maximum rent', blank=True, null=True, default=0)
#     pl_file = m.FileField('P&L excel file', upload_to=upload_file, blank=True, null=True)
#     radius = m.IntegerField('Radius by meter /limit 1km/', blank=True, null=True, default=0)
#     turnover_rent_percent = m.IntegerField('Turnover rent percentage', blank=True, null=True, default=0)
#     address = m.CharField('Address', blank=False, default='', max_length=200)
#     cluster = m.CharField('Cluster', blank=True, null=True, max_length=500)
#
#     addr1_prov = m.ForeignKey(City, on_delete=m.SET_NULL, null=True, blank=True, verbose_name='City and Aimag')
#     addr2_dist = m.ForeignKey(District, on_delete=m.SET_NULL, null=True, blank=True, verbose_name='District and Sum')
#     address_det = m.CharField('Address detail', blank=True, default='', max_length=500)
#     sp_name = m.CharField('SP name', blank=True, default='', max_length=50)
#     near_gs_cvs = m.IntegerField('GS25 number', blank=True, null=True, default=0)
#     near_school = m.IntegerField('School number', blank=True, null=True, default=0)
#     park_slot = m.IntegerField('Park number', blank=True, default=0)
#     floor = m.IntegerField('Floor number', blank=True, default=0)
#     cont_st_dt = m.DateField('Rent agreement start date', blank=True, null=True)
#     cont_ed_dt = m.DateField('Rent agreement end date', blank=True, null=True)
#     zip_code = m.CharField('Zip code', blank=True, default='', max_length=100)
#     rent_tp = m.BooleanField('Type of rent agreement', blank=True, null=True)
#     rent_near = m.CharField('Company name', blank=True, default='', max_length=50)
#     adv = m.CharField('Advantage', blank=True, default='', max_length=100)
#     disadv = m.CharField('Disadvantage', blank=True, default='', max_length=100)
#     propose = m.TextField('Suggestions for improvement', blank=True, null=True)
#     created_date = m.DateTimeField('Created date', auto_now_add=True)
#     modified_date = m.DateTimeField('Modified date', auto_now=True)
#     created_by = m.ForeignKey(User, verbose_name='Created by', related_name='store_planning_created',
#                               on_delete=m.PROTECT, null=True)
#     modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='store_planning_modified',
#                                on_delete=m.PROTECT, null=True)
#
#     def __str__(self):
#         return self.store_id
#
#     def save(self, *args, **kwargs):
#         if not self.pk and not self.created_by:
#             self.created_by = self.modified_by
#         super(StorePlanning, self).save(*args, **kwargs)
#
#     class Meta:
#         db_table = 'store_planning'
#         verbose_name = 'Store Planning'
