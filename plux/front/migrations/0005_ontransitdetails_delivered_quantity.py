# Generated by Django 4.1.4 on 2022-12-21 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_ontransitheader_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ontransitdetails',
            name='delivered_quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
