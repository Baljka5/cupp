# Generated by Django 2.1.7 on 2024-03-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_consultant', '0018_auto_20240319_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storeconsultant',
            old_name='storabox',
            new_name='ser_storabox',
        ),
        migrations.RemoveField(
            model_name='storeconsultant',
            name='Umoney',
        ),
        migrations.RemoveField(
            model_name='storeconsultant',
            name='near_store',
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='am_num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Дэлгүүрийн туслах менежерийн тоо'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='ser_Umoney',
            field=models.BooleanField(blank=True, null=True, verbose_name='Автобусны карт цэнэглэгчтэй эсэх'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='ser_delivery',
            field=models.BooleanField(blank=True, null=True, verbose_name='Хүргэлт'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='ser_lottery',
            field=models.BooleanField(blank=True, null=True, verbose_name='Сугалаа'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='ser_pow_bank',
            field=models.BooleanField(blank=True, null=True, verbose_name='Зөөврийн цэнэглэгч түрээс'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='ser_print',
            field=models.BooleanField(blank=True, null=True, verbose_name='Хэвлэл'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='ser_ticket',
            field=models.BooleanField(blank=True, null=True, verbose_name='Тасалбар'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='sm_num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Дэлгүүрийн менежерийн тоо'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='toilet_tp',
            field=models.BooleanField(blank=True, null=True, verbose_name='00-н төрөл (Өөрийн, нийтийн)'),
        ),
    ]