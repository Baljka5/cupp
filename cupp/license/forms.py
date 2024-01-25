from django import forms as f
from django.conf import settings
from .models import MainTable


class MainTableForm(f.ModelForm):
    st_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    ed_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = MainTable
        fields = ['store_id', 'lic_id', 'lic_id_nm', 'lic_yn', 'st_dt', 'ed_dt', 'lic_owner', 'lic_prov_ID',
                  'lic_prov_name',
                  'lic_no']
        widgets = {'store_id': f.TextInput(attrs={'class': 'form-control'}),
                   'lic_id_nm': f.TextInput(attrs={'class': 'form-control'}),
                   'lic_owner': f.TextInput(attrs={'class': 'form-control'}),
                   'lic_prov_ID': f.TextInput(attrs={'class': 'form-control'}),
                   'lic_prov_name': f.TextInput(attrs={'class': 'form-control'}),
                   'lic_no': f.TextInput(attrs={'class': 'form-control'}),
                   }
