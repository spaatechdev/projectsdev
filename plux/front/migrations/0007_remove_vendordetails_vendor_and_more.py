# Generated by Django 4.1.4 on 2023-01-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0006_vendordetails_customerdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendordetails',
            name='vendor',
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_email',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_no',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='contact_email',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='contact_no',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='storemaster',
            name='contact_email',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='storemaster',
            name='contact_no',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='vendormaster',
            name='contact_email',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='vendormaster',
            name='contact_no',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name='CustomerDetails',
        ),
        migrations.DeleteModel(
            name='VendorDetails',
        ),
    ]