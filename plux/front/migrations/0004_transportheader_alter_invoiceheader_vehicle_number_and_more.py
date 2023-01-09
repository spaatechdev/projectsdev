# Generated by Django 4.1.4 on 2023-01-06 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_invoiceheader_invoice_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transporter_name', models.CharField(max_length=100)),
                ('vehicle_number', models.CharField(max_length=10)),
                ('vehicle_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='invoiceheader',
            name='vehicle_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='ontransitheader',
            name='transfer_number',
            field=models.CharField(blank=True, default='TR-00000001', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorderheader',
            name='purchase_order_no',
            field=models.CharField(default='PO-00000001', max_length=15),
        ),
        migrations.AlterField(
            model_name='salesorderheader',
            name='sales_order_no',
            field=models.CharField(default='SO-00000001', max_length=15),
        ),
        migrations.CreateModel(
            name='DeliveryChallanHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_challan_number', models.CharField(default='DC-00000001', max_length=15)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(default=1)),
                ('deleted', models.BooleanField(default=0)),
                ('invoice_header', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='front.invoiceheader')),
                ('sales_order_header', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='front.salesorderheader')),
                ('transport_header', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='front.transportheader')),
            ],
            options={
                'verbose_name_plural': 'delivery_challan_header',
                'db_table': 'delivery_challan_header',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DeliveryChallanDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deleted', models.BooleanField(default=0)),
                ('delivery_challan_header', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='front.deliverychallanheader')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DeliveryItem', to='front.itemmaster')),
            ],
            options={
                'verbose_name_plural': 'delivery_challan_details',
                'db_table': 'delivery_challan_details',
                'managed': True,
            },
        ),
    ]