# Generated by Django 3.1.5 on 2021-02-03 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodotti', '0014_auto_20210203_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
