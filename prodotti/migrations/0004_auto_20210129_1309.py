# Generated by Django 3.1.5 on 2021-01-29 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodotti', '0003_auto_20210122_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, max_length=2083, upload_to=''),
        ),
    ]
