# Generated by Django 2.1.7 on 2019-02-27 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0013_point_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='bep',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Breakeven point'),
        ),
        migrations.AlterField(
            model_name='point',
            name='deposit',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Deposit'),
        ),
        migrations.AlterField(
            model_name='point',
            name='expected_sales',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Expected daily sales'),
        ),
        migrations.AlterField(
            model_name='point',
            name='hh',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Households in the direct area'),
        ),
        migrations.AlterField(
            model_name='point',
            name='office',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Office people in the direct area'),
        ),
        migrations.AlterField(
            model_name='point',
            name='passers',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Average passers an hour'),
        ),
        migrations.AlterField(
            model_name='point',
            name='radius',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Radius by meter /limit 1km/'),
        ),
        migrations.AlterField(
            model_name='point',
            name='students',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='School/University students in the direct area'),
        ),
    ]
