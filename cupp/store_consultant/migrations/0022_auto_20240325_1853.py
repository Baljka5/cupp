# Generated by Django 2.1.7 on 2024-03-25 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_consultant', '0021_auto_20240325_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeconsultant',
            name='am_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='Дэлгүүрийн туслах менежерийн тоо'),
        ),
        migrations.AlterField(
            model_name='storeconsultant',
            name='sm_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='Дэлгүүрийн менежерийн тоо'),
        ),
        migrations.AlterField(
            model_name='storeconsultant',
            name='tv_screen',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tv screen'),
        ),
    ]
