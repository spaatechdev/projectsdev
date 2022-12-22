# Generated by Django 4.1.4 on 2022-12-22 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0010_physicalstockheader_physicalstockdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='physicalstockdetails',
            name='original_quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='storetransactionheader',
            name='physical_stock_header',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='front.physicalstockheader'),
        ),
        migrations.AlterField(
            model_name='physicalstockdetails',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
