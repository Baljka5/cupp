# Generated by Django 2.1.7 on 2024-02-15 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0006_auto_20240201_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintable',
            name='lic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_table_lic_id', to='license.DimensionTable', verbose_name='License type'),
        ),
        migrations.AlterField(
            model_name='maintable',
            name='lic_id_nm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_table_lic_id_nm', to='license.DimensionTable', verbose_name='License type name'),
        ),
    ]