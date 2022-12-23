# Generated by Django 4.1.4 on 2022-12-22 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0009_alter_storetransactiondetails_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicalStockHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_stock_check_number', models.CharField(blank=True, max_length=15, null=True)),
                ('physical_stock_check_date', models.DateField(blank=True, null=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('deleted', models.BooleanField(default=0)),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PhysicalStockStore', to='front.storemaster')),
            ],
            options={
                'verbose_name_plural': 'physical_stock_header',
                'db_table': 'physical_stock_header',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PhysicalStockDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deleted', models.BooleanField(default=0)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PhysicalStockItem', to='front.itemmaster')),
                ('physical_stock_header', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='front.physicalstockheader')),
            ],
            options={
                'verbose_name_plural': 'physical_stock_details',
                'db_table': 'physical_stock_details',
                'managed': True,
            },
        ),
    ]