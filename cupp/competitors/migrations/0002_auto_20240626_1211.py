# Generated by Django 2.1.7 on 2024-06-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storecompetitors',
            name='comp_latt',
            field=models.CharField(blank=True, default=0, max_length=50, null=True, verbose_name='Өрсөлдөгчийн Өргөрөг'),
        ),
        migrations.AlterField(
            model_name='storecompetitors',
            name='comp_long',
            field=models.CharField(blank=True, default=0, max_length=50, null=True, verbose_name='Өрсөлдөгчийн Уртраг'),
        ),
        migrations.AlterField(
            model_name='storecompetitors',
            name='comp_pros',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Өрсөлдөгчийн давуу тал'),
        ),
    ]