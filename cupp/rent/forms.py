from django import forms as f
from django.conf import settings
from .models import StrRent


class StrRentForm(f.ModelForm):
    st_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    ed_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    ext_ed_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    hand_over_dt = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = StrRent
        fields = ['store_id', 'str_name', 'str_address', 'lesser1', 'lesser2', 'phone_number1', 'phone_number2',
                  'email', 'area_size', 'cont_link', 'cont_type', 'cntr_num1', 'cntr_num2', 'st_dt', 'ed_dt',
                  'ext_ed_dt', 'hand_over_dt', 'rent_mo_fee', 'rent_mo_fee_annex1', 'rent_mo_fee_annex2',
                  'deposit_amount', 'association_no', 'association_fee', 'manage_fee', 'manage_cnt_no', 'exp_inc',
                  'other_cont', 'stora_yn', 'stora_fee', 'atm_fee', 'atm_yn', 'sublet_yn', 'sublet1_rent',
                  'sublet2_rent', 'sublet1_size', 'sublet2_size', 'sublet1_deposit', 'sublet2_deposit',
                  'sublet1_cnt_no', 'sublet2_cnt_no', 'letter', 'notice', 'notariat_yn', 'other_cnt', 'franchise_yn',
                  'fr_rent_yn', 'dedication', 'real_estate_yn', 'special_terms', 'cont_resp_term', 'lesser3',
                  'phone_number3', 'cntr_num3', 'sublet3_rent', 'sublet3_size', 'sublet3_deposit', 'sublet3_cnt_no',
                  'rent_mo_fee_annex3'
                  ]

        # widgets = {'store_no': f.TextInput(attrs={'class': 'form-control'}),
        #            'store_name': f.TextInput(attrs={'class': 'form-control'}),
        #            'activ_desc': f.Textarea(attrs={'class': 'form-control'}),
        #            'resp_action': f.Textarea(attrs={'class': 'form-control'}),
        #            }
