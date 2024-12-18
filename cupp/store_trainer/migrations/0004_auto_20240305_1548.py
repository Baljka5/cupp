# Generated by Django 2.1.7 on 2024-03-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_trainer', '0003_auto_20240304_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='storetrainer',
            name='cam_ext',
            field=models.IntegerField(blank=True, default=0, verbose_name='External camera'),
        ),
        migrations.AddField(
            model_name='storetrainer',
            name='cam_int',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Camera'),
        ),
        migrations.AddField(
            model_name='storetrainer',
            name='hard_disk_size_tb',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Hard disk size'),
        ),
        migrations.AddField(
            model_name='storetrainer',
            name='monitor_eq',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Recording device information'),
        ),
        migrations.AddField(
            model_name='storetrainer',
            name='pos_qty',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='POS'),
        ),
        migrations.AddField(
            model_name='storetrainer',
            name='video_storage_day',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Days to keep records'),
        ),
    ]
