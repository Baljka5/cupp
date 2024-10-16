from django.db import models

# Create your models here.
from django.db import models
import os
import uuid

from django.db import models as m
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from uuid import uuid4
from django.utils import timezone

from cupp.point.models import District, City
from cupp.event.models import ActionOwner


# Create your models here.
class DisputeTable(models.Model):
    five_digit_validator = RegexValidator(r'^\d{5}$', 'Store number must be a 5-digit number')
    date = models.DateField('Бодит үйл явдал болсон огноо')
    store_no = models.CharField('Үйл явдал болсон дэлгүүрийн дугаар', max_length=5, validators=[five_digit_validator],
                                blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    disp_desc = models.TextField('Болсон хэргийн талаар дэлгэрэнгүй мэдээлэл')
    disp_cat = models.CharField('Хэргийн төрөл', max_length=50)
    dmg_amt = models.FloatField('Хохирлын хэмжээ /мөнгөн дүн/', default=0)
    dmg_uom = models.CharField('Хохирлын хэмжигдэхүүн', max_length=255)
    disp_owner = models.ForeignKey(ActionOwner, on_delete=m.CASCADE)
    disp_status = models.BooleanField('Хэргийн төлөв', blank=True, null=True)
    disp_progress = models.CharField('Хэргийн явц', max_length=500, blank=True, null=True)
    disp_result = models.BooleanField('Хэрэг шийдэгдсэн эсэх', blank=True, null=True)
    close_date = models.DateField('Хэрэг шийдэгдсэн өдөр', blank=True, null=True)
    supp_link = models.URLField('Холбогдох баримт бичгийн холбоос', blank=True, null=True)

    created_date = m.DateTimeField('Created date', auto_now_add=True, null=True)
    modified_date = m.DateTimeField('Modified date', auto_now=True, null=True)
    created_by = m.ForeignKey(User, verbose_name='Created by', related_name='dispute_created',
                              on_delete=m.PROTECT, null=True, blank=True)
    modified_by = m.ForeignKey(User, verbose_name='Modified by', related_name='dispute_modified',
                               on_delete=m.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.disp_cat

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_by:
            self.created_by = self.modified_by
        super(DisputeTable, self).save(*args, **kwargs)

    class Meta:
        db_table = 'dispute'
        verbose_name = 'DisputeTable'
