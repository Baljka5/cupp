# Generated by Django 2.1.7 on 2023-12-25 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0016_auto_20231225_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(default='', max_length=50, unique=True, verbose_name='City and aimag name')),
                ('sum_name', models.CharField(default='', max_length=50, unique=True, verbose_name='Sum name')),
            ],
            options={
                'verbose_name': 'City',
                'db_table': 'cupp_city',
            },
        ),
    ]
