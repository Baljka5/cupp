# Generated by Django 2.1.7 on 2024-01-23 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('license', '0003_auto_20240122_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='DimensionTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lic_id', models.CharField(default='', max_length=50, verbose_name='License type')),
                ('lic_id_nm', models.CharField(default='', max_length=50, verbose_name='License type name')),
            ],
            options={
                'verbose_name': 'Dimenstion table',
                'db_table': 'lic_type',
            },
        ),
        migrations.CreateModel(
            name='DimensionTableLicenseProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lic_prov_name', models.CharField(max_length=50, verbose_name='License Provider Name')),
                ('org_add', models.CharField(max_length=50, verbose_name='License Provider Address')),
                ('org_emp_nm', models.CharField(max_length=50, verbose_name='Name of concerned employee')),
                ('org_emp_tel', models.CharField(max_length=50, verbose_name='Name of concerned telephone')),
                ('org_emp_em', models.CharField(max_length=50, verbose_name='Name of concerned employee email')),
            ],
            options={
                'verbose_name': 'Dimenstion table',
                'db_table': 'lic_provider',
            },
        ),
        migrations.CreateModel(
            name='MainTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=50, verbose_name='Store ID')),
                ('lic_id_nm', models.CharField(blank=True, max_length=50, verbose_name='License Type Name')),
                ('lic_yn', models.BooleanField(blank=True, null=True, verbose_name='Type of rent agreement')),
                ('st_dt', models.DateField(blank=True, null=True, verbose_name='Rent agreement start date')),
                ('ed_dt', models.DateField(blank=True, null=True, verbose_name='License Ended Date')),
                ('lic_owner', models.CharField(max_length=50, verbose_name='Licensed Employee')),
                ('lic_prov_ID', models.CharField(max_length=50, verbose_name='License Provider ID')),
                ('lic_prov_name', models.CharField(max_length=50, verbose_name='License Provider Name')),
                ('lic_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='License Code')),
                ('lic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='license.DimensionTable', verbose_name='License type')),
            ],
            options={
                'verbose_name': 'MainTable',
                'db_table': 'str_license',
            },
        ),
        migrations.AddField(
            model_name='dimensiontablelicenseprovider',
            name='lic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='license.MainTable', verbose_name='License Provider ID'),
        ),
    ]