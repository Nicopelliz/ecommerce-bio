# Generated by Django 3.1.5 on 2021-02-05 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prodotti', '0021_auto_20210205_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='prodotti.orderitem'),
            preserve_default=False,
        ),
    ]
