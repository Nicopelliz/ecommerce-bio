# Generated by Django 3.1.5 on 2021-02-05 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prodotti', '0023_auto_20210205_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
    ]
