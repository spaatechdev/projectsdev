# Generated by Django 4.1.4 on 2022-12-14 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
