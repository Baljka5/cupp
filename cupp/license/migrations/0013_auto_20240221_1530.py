# Generated by Django 2.1.7 on 2024-02-21 15:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0012_auto_20240215_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintable',
            name='alc_closetime',
            field=models.TimeField(default=django.utils.timezone.now, null=True, verbose_name='Time to sell out alchohol'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='alc_opentime',
            field=models.TimeField(default=django.utils.timezone.now, null=True, verbose_name='Time to start selling alcohol'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='camera_cnt',
            field=models.IntegerField(null=True, verbose_name='Total number of cameras'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='ed_dt',
            field=models.DateField(null=True, verbose_name='License Ended Date'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='lic_id_nm',
            field=models.CharField(max_length=50, null=True, verbose_name='License Type Name'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='lic_owner',
            field=models.CharField(max_length=50, null=True, verbose_name='Licensed Employee'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='lic_yn',
            field=models.BooleanField(null=True, verbose_name='Type of rent agreement'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='st_dt',
            field=models.DateField(null=True, verbose_name='Rent agreement start date'),
        ),
    ]
