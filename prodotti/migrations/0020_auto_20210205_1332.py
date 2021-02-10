# Generated by Django 3.1.5 on 2021-02-05 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prodotti', '0019_auto_20210203_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='city',
            new_name='citta',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zip_code',
            new_name='codice_postale',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='indirizzo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='provincia',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
