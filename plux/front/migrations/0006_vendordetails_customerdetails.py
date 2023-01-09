# Generated by Django 4.1.4 on 2023-01-09 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_countries_phonecode'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_name', models.CharField(blank=True, max_length=30, null=True)),
                ('attribute_value', models.TextField(blank=True, null=True)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='front.vendormaster')),
            ],
            options={
                'verbose_name_plural': 'vendor_details',
                'db_table': 'vendor_details',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_name', models.CharField(blank=True, max_length=30, null=True)),
                ('attribute_value', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='front.customer')),
            ],
            options={
                'verbose_name_plural': 'customer_details',
                'db_table': 'customer_details',
                'managed': True,
            },
        ),
    ]
