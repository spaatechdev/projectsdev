# Generated by Django 4.1.4 on 2022-12-24 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0018_invoiceheader_invoicedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='storetransactionheader',
            name='invoice_header',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='front.invoiceheader'),
        ),
    ]
