# Generated by Django 4.1.4 on 2022-12-26 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceterms',
            old_name='invoice_header_id',
            new_name='invoice_header',
        ),
    ]