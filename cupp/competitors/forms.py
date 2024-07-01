from django import forms as f
from django.conf import settings
from cupp.competitors.models import StoreCompetitors


class StoreCompetitorsForm(f.ModelForm):
    comp_open_dt = f.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    comp_close_dt = f.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    COMP_SCHEDULE_TP_CHOICES = [
        ('24H', '24H'),
        ('17H', '17H'),
        ('SPECIFIC', 'SPECIFIC')
    ]
    comp_schedule_tp = f.ChoiceField(choices=COMP_SCHEDULE_TP_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                                     required=False)
    # comp_schedule_time = f.TimeField(required=False, input_formats=['%H:%M:%S'],
    #                                  widget=f.TimeInput(attrs={'type': 'time', 'step': '1'}))

    class Meta:
        model = StoreCompetitors
        fields = "__all__"
