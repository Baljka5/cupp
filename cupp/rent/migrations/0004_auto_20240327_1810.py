# Generated by Django 2.1.7 on 2024-03-27 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_auto_20240327_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='strrent',
            old_name='other_cnt',
            new_name='other_cont',
        ),
    ]