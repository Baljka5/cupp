from django.forms import ClearableFileInput


class ClearableFileInput(ClearableFileInput):
    template_name = 'clearable_file_input.html'
