# Generated by Django 2.1.7 on 2024-01-25 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20240125_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedailylog',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='store_daily_logs', to=settings.AUTH_USER_MODEL, verbose_name='Creadted by'),
        ),
    ]