# Generated by Django 2.1.7 on 2024-02-22 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20240201_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='storedailylog',
            name='consequences',
            field=models.BooleanField(blank=True, null=True, verbose_name='Consequences of events'),
        ),
    ]