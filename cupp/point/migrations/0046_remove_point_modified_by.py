# Generated by Django 2.1.7 on 2024-02-23 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0045_auto_20240223_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='modified_by',
        ),
    ]
