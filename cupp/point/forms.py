from django import forms as f
from django.conf import settings

from cupp.common.fields import ClearableFileInput

from .models import Point, PointPhoto


class PointForm(f.ModelForm):
    available_date = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    cont_st_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    cont_ed_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    # type = f.ModelChoiceField(queryset=Type.objects.all(), required=True, label='Type', empty_label=None)

    class Meta:
        model = Point
        fields = ('type', 'lat', 'lon',
                  'owner_name', 'owner_phone', 'owner_email',
                  'base_rent_rate', 'max_rent_rate', 'proposed_layout',
                  'availability', 'available_date', 'size', 'grade',
                  'deposit', 'bep', 'expected_sales', 'passers', 'hh',
                  'office', 'students', 'turnover_rent_percent', 'radius',
                  'isr_file', 'pl_file', 'address', 'addr1_prov', 'addr2_dist',
                  'address_det', 'sp_name', 'near_gs_cvs', 'near_school', 'park_slot',
                  'floor', 'cont_st_dt', 'cont_ed_dt', 'zip_code', 'rent_tp', 'rent_near',
                  'adv', 'disadv', 'propose'
                  )
        widgets = {
            'proposed_layout': ClearableFileInput(),
            'isr_file': ClearableFileInput(),
            'pl_file': ClearableFileInput(),
        }


PhotoFormset = f.inlineformset_factory(Point, PointPhoto, fields=['photo'], extra=6)
