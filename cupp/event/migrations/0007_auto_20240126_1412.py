# Generated by Django 2.1.7 on 2024-01-26 14:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20240126_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedailylog',
            name='store_no',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^\\d{5}$', 'Store number must be a 5-digit number')]),
        ),
    ]