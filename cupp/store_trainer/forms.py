from django import forms as f
from django.conf import settings
from cupp.store_trainer.models import StoreTrainer


class StoreTrainerForm(f.ModelForm):
    planned_date = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    displayed_date = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    open_date = f.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = StoreTrainer
        fields = ['store_id', 'store_name', 'size', 'sitting_size', 'war_size', 'toilet_size', 'resale_size', 'shelf',
                  'wall_shelf', 'cash_shelf', 'st_name', 'chair_size', 'desk_size', 'planned_date', 'displayed_date',
                  'open_date', 'open_time', 'light_box', 'sand_grill', 'slushie_mach', 'icecream_mach', 'mcs_mach',
                  'disp_5_mach', 'disp_3_mach', 'horizontal_freeze', 'coffee_mach_button', 'coffee_mach_led', 'steamer',
                  'can_warmer', 'food_warmer', 'vertical_freezer', 'dogbuggi_cooker', 'hot_water_disp', 'tv_screen',
                  'pos_qty', 'cam_int', 'cam_ext', 'monitor_eq', 'hard_disk_size_tb', 'video_storage_day']
