# Generated by Django 2.1.7 on 2024-02-15 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0009_auto_20240215_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintable',
            name='lic_id_nm',
        ),
    ]
