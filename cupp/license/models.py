from django.db import models

# Create your models here.
from django.db import models
import os
import uuid

from django.db import models as m
from django.contrib.auth.models import User
from django.conf import settings
from uuid import uuid4


class DimensionTable(m.Model):
    lic_id = m.CharField('License type', blank=False, default='', max_length=50)
    lic_id_nm = m.CharField('License type name', blank=False, default='', max_length=50)

    def __str__(self):
        return self.lic_id

    class Meta:
        db_table = 'lic_type'
        verbose_name = 'Dimenstion table'

class MainTable(models.Model):
    store_id = models.CharField('Store ID', max_length=50)
    lic_id = models.ForeignKey(DimensionTable, on_delete=models.CASCADE, verbose_name='License type')
    lic_id_nm = models.CharField('License Type Name', max_length=50, blank=True)
    lic_yn = models.BooleanField('Type of rent agreement', blank=True, null=True)
    st_dt = models.DateField('Rent agreement start date', blank=True, null=True)
    ed_dt = models.DateField('License Ended Date', blank=True, null=True)
    lic_owner = models.CharField('Licensed Employee', max_length=50)
    lic_prov_ID = models.CharField('License Provider ID', max_length=50)
    lic_prov_name = models.CharField('License Provider Name', max_length=50)
    lic_no = models.CharField('License Code', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'str_license'
        verbose_name = 'MainTable'


class DimensionTableLicenseProvider(models.Model):
    lic_id = models.ForeignKey(MainTable, on_delete=models.CASCADE, verbose_name='License Provider ID')
    lic_prov_name = models.CharField('License Provider Name', max_length=50)
    org_add = models.CharField('License Provider Address', max_length=50)
    org_emp_nm = models.CharField('Name of concerned employee', max_length=50)
    org_emp_tel = models.CharField('Name of concerned telephone', max_length=50)
    org_emp_em = models.CharField('Name of concerned employee email', max_length=50)

    def __str__(self):
        return self.lic_prov_id

    class Meta:
        db_table = 'lic_provider'
        verbose_name = 'Dimenstion table'

# lic_id_nm = m.ForeignKey(dimension_table.lic_id_nm, on_delete=m.CASCADE, related_name='License name')
