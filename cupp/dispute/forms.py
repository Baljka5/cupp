from django import forms as f
from django.conf import settings
from .models import DisputeTable
from cupp.point.models import District, City
from cupp.event.models import ActionOwner


class DisputeForm(f.ModelForm):
    date = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    close_date = f.DateField(
        required=False,
        input_formats=settings.DATE_INPUT_FORMATS,
    )
    disp_desc = f.CharField(widget=f.Textarea(attrs={'class': 'form-control'}))
    dmg_amt = f.FloatField(widget=f.NumberInput(attrs={'class': 'form-control'}))
    supp_link = f.URLField(widget=f.URLInput(attrs={'class': 'form-control'}))
    disp_cat = f.ChoiceField(
        choices=[('', '---------'), ('ТАНХАЙ', 'ТАНХАЙ'), ('ДЭЭРЭМ', 'ДЭЭРЭМ'), ('ХУЛГАЙ', 'ХУЛГАЙ'),
                 ('ЗӨРЧИЛ', 'ЗӨРЧИЛ'), ('БУСАД', 'БУСАД')],
        widget=f.Select(attrs={'class': 'form-control'})
    )
    STATUS_CHOICE = [
        ('', '---------'),
        (True, 'Хаагдсан'),
        (False, 'Нээлттэй'),
    ]

    disp_status = f.ChoiceField(
        choices=STATUS_CHOICE,
        widget=f.Select(attrs={'class': 'form-control'}),
        initial=False  # Default to 'Нээлттэй'
    )

    RESULT_CHOICE = [
        ('', '---------'),
        (True, 'Yes'),
        (False, 'No')
    ]

    disp_result = f.ChoiceField(
        choices=RESULT_CHOICE,
        widget=f.Select(attrs={'class': 'form-control'}),
        initial=False  # Default to 'No'
    )

    store_no = f.CharField(widget=f.TextInput(attrs={'class': 'form-control'}), required=True)
    store_name = f.CharField(widget=f.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), required=True)

    class Meta:
        model = DisputeTable
        fields = ['date', 'store_no', 'store_name', 'disp_desc', 'disp_cat', 'dmg_amt', 'dmg_uom',
                  'disp_status', 'disp_progress', 'disp_result', 'supp_link', 'disp_owner', 'close_date']
