# Generated by Django 2.1.7 on 2024-02-26 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0018_auto_20240223_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintable',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='maintable',
            name='modified_by',
        ),
    ]
