# Generated by Django 4.1.4 on 2022-12-26 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_rename_invoice_header_id_invoiceterms_invoice_header'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceterms',
            old_name='term_id',
            new_name='term',
        ),
    ]