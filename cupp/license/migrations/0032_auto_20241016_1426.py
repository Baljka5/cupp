# Generated by Django 2.1.7 on 2024-10-16 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0031_auto_20241009_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disputetable',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='disputetable',
            name='disp_owner',
        ),
        migrations.RemoveField(
            model_name='disputetable',
            name='modified_by',
        ),
        migrations.DeleteModel(
            name='DisputeTable',
        ),
    ]
