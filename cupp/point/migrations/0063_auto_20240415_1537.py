# Generated by Django 2.1.7 on 2024-04-15 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0062_auto_20240411_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='district_name',
            field=models.CharField(default='', max_length=50, verbose_name='District and sum name'),
        ),
    ]