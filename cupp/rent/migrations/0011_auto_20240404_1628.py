# Generated by Django 2.1.7 on 2024-04-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0010_auto_20240401_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strrent',
            name='cont_type',
            field=models.CharField(blank=True, choices=[('Үндсэн', 'Үндсэн'), ('Сунгалт', 'Сунгалт'), ('Нэмэлт', 'Нэмэлт')], max_length=10, null=True, verbose_name='Contract Type'),
        ),
    ]
