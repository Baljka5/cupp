from django import forms as f
from django.conf import settings

from cupp.common.fields import ClearableFileInput

from .models import Point, PointPhoto


class PointForm(f.ModelForm):
    available_date = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Point
        fields = ('type', 'lat', 'lon',
                  'owner_name', 'owner_phone', 'owner_email',
                  'base_rent_rate', 'max_rent_rate', 'proposed_layout',
                  'availability', 'available_date', 'size', 'type', 'grade',
                  'deposit', 'bep', 'expected_sales', 'passers', 'hh',
                  'office', 'students', 'turnover_rent_percent', 'radius',
                  'isr_file', 'pl_file', 'address'
                  )
        widgets = {
            'proposed_layout': ClearableFileInput(),
            'isr_file': ClearableFileInput(),
            'pl_file': ClearableFileInput(),
        }


PhotoFormset = f.inlineformset_factory(Point, PointPhoto, fields=['photo'], extra=6)
