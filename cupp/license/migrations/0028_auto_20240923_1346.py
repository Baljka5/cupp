# Generated by Django 2.1.7 on 2024-09-23 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0027_auto_20240920_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintable',
            name='alc_type',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Type of Alcohol'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='lic_type',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Type of License'),
        ),
    ]
