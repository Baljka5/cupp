# Generated by Django 2.1.7 on 2024-10-14 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('veritech_api', '0004_auto_20241010_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('employee_code', models.CharField(max_length=50)),
                ('origin_name', models.CharField(blank=True, max_length=100)),
                ('urag', models.CharField(blank=True, max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('state_reg_number', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('employee_phone', models.CharField(max_length=20)),
                ('post_address', models.CharField(blank=True, max_length=255)),
                ('education_level', models.CharField(blank=True, max_length=50)),
                ('marital_status', models.CharField(blank=True, max_length=50)),
                ('no_of_family_members', models.IntegerField(blank=True, null=True)),
                ('no_of_children', models.IntegerField(blank=True, null=True)),
                ('department_name', models.CharField(max_length=255)),
                ('position_name', models.CharField(max_length=255)),
                ('insured_type_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type_name', models.CharField(max_length=255)),
                ('city_name', models.CharField(max_length=255)),
                ('district_name', models.CharField(max_length=255)),
                ('street_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='veritech_api.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_account_number', models.CharField(max_length=50)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banks', to='veritech_api.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('mobile', models.CharField(max_length=20)),
                ('work_name', models.CharField(blank=True, max_length=255)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='veritech_api.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeWorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=255)),
                ('department_name', models.CharField(max_length=255)),
                ('position_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_experiences', to='veritech_api.Employee')),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='employeeid',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='employeeid',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='employeeid',
        ),
        migrations.RemoveField(
            model_name='family',
            name='employeeid',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Bank',
        ),
        migrations.DeleteModel(
            name='Experience',
        ),
        migrations.DeleteModel(
            name='Family',
        ),
        migrations.DeleteModel(
            name='General',
        ),
    ]
