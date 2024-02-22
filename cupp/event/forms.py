from django import forms as f
from django.conf import settings
from .models import ActionCategory, ActionOwner, StoreDailyLog


class StoreDailyLogForm(f.ModelForm):
    date = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    CONSEQUENCES_CHOICES = [
        ('', '---------'),
        (True, 'Сайн'),  # Represents True
        (False, 'Муу'),  # Represents False
    ]

    consequences = f.ChoiceField(choices=CONSEQUENCES_CHOICES, widget=f.Select(attrs={'class': 'form-control'}),
                                 required=False)

    class Meta:
        model = StoreDailyLog
        fields = ['date', 'store_no', 'store_name', 'activ_cat', 'activ_desc', 'resp_action', 'action_owner',
                  'consequences']

        widgets = {'store_no': f.TextInput(attrs={'class': 'form-control'}),
                   'store_name': f.TextInput(attrs={'class': 'form-control'}),
                   'activ_desc': f.Textarea(attrs={'class': 'form-control'}),
                   'resp_action': f.Textarea(attrs={'class': 'form-control'}),
                   }
