# Generated by Django 3.1.5 on 2021-02-02 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodotti', '0009_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(editable=False, max_length=200, unique=True),
        ),
    ]
