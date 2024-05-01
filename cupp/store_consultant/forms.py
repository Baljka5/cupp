from django import forms as f
from django.conf import settings
from cupp.store_consultant.models import StoreConsultant


class StoreConsultantForm(f.ModelForm):
    close_date = f.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    CONSEQUENCES_CHOICES = [
        ('', '---------'),
        (True, 'Тийм'),
        (False, 'Үгүй'),
    ]
    TOILET_TYPE_CHOICES = [
        ('', '---------'),
        (True, 'Нийтийн'),
        (False, 'Өөрийн'),
    ]
    TT_TYPE_CHOICES = [
        ('24H', '24H'),
        ('17H', '17H'),
        ('SPECIFIC', 'SPECIFIC')
    ]
    tt_type = f.ChoiceField(choices=TT_TYPE_CHOICES, widget=f.Select(attrs={'class': 'form-control'}), required=False)
    ser_storabox = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                                 required=False)
    ser_Umoney = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                               required=False)
    ser_pow_bank = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                                 required=False)
    ser_lottery = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                                required=False)
    ser_delivery = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                                 required=False)
    ser_print = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                              required=False)
    ser_ticket = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                               required=False)
    toilet_tp = f.ChoiceField(choices=TOILET_TYPE_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                              required=False)

    wday_hours = f.TimeField(required=False, input_formats=['%H:%M:%S'],
                             widget=f.TimeInput(attrs={'type': 'time', 'step': '1'})
                             )
    wend_hours = f.TimeField(required=False, input_formats=['%H:%M:%S'],
                             widget=f.TimeInput(attrs={'type': 'time', 'step': '1'})
                             )

    class Meta:
        model = StoreConsultant
        fields = "__all__"
