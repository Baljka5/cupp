# Generated by Django 2.1.7 on 2019-02-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0007_remove_point_available_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='available_date',
            field=models.DateField(blank=True, null=True, verbose_name='Available date'),
        ),
    ]