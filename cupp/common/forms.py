from django import forms as f


class MySettingsForm(f.Form):
    first_name = f.CharField(label='Өөрийн нэр')
    last_name = f.CharField(label='Эцэг /эх/-ийн нэр')
