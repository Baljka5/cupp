# Generated by Django 2.1.7 on 2024-10-22 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_consultant', '0041_auto_20241022_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='tags',
            field=models.TextField(blank=True, null=True, verbose_name='Tags and Store IDs'),
        ),
    ]