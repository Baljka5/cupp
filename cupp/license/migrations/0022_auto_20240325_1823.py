# Generated by Django 2.1.7 on 2024-03-25 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0021_auto_20240226_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintable',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='main_table_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='main_table_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modified by'),
        ),
    ]
