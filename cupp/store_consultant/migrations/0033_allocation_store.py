# Generated by Django 2.1.7 on 2024-06-17 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_consultant', '0032_auto_20240617_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocation',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_consultant.StoreConsultant'),
        ),
    ]