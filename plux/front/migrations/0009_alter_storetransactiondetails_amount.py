# Generated by Django 4.1.4 on 2022-12-22 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0008_alter_storetransactiondetails_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storetransactiondetails',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
