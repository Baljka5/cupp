# Generated by Django 2.1.7 on 2024-01-09 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0019_auto_20231225_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(default='', max_length=50, unique=True, verbose_name='Type name')),
                ('type_cd', models.CharField(default='', max_length=50, unique=True, verbose_name='Type code')),
                ('icon', models.ImageField(upload_to='../../.store/static/images/ui/')),
            ],
            options={
                'verbose_name': 'District',
                'db_table': 'cupp_type',
            },
        ),
    ]