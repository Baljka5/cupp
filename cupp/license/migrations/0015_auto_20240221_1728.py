# Generated by Django 2.1.7 on 2024-02-21 17:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0014_auto_20240221_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintable',
            name='alc_closetime',
            field=models.TimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Time to sell out alchohol'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='alc_opentime',
            field=models.TimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Time to start selling alcohol'),
        ),
    ]