# Generated by Django 2.1.7 on 2024-03-04 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_consultant', '0003_area_consultants'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeconsultant',
            name='near_gs',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='GS detail status'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='prc_grade',
            field=models.BooleanField(blank=True, null=True, verbose_name='Pricing policy'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='sm_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Store manager name'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='sm_phone',
            field=models.IntegerField(blank=True, null=True, verbose_name='Store manager phone'),
        ),
        migrations.AddField(
            model_name='storeconsultant',
            name='store_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Store Name'),
        ),
        migrations.AlterField(
            model_name='storeconsultant',
            name='store_id',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Store ID'),
        ),
    ]