# Generated by Django 3.1.5 on 2021-01-22 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prodotti', '0002_auto_20210122_1159'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Food',
            new_name='Product',
        ),
    ]