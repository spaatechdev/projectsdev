# Generated by Django 4.1.4 on 2022-12-22 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0012_physicalstockdetails_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicalstockdetails',
            name='status',
        ),
    ]
