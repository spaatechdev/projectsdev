# Generated by Django 4.1.4 on 2023-01-09 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_transportheader_alter_invoiceheader_vehicle_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='countries',
            name='phonecode',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
