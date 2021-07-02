# Generated by Django 3.1.5 on 2021-02-03 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prodotti', '0017_auto_20210203_2131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['ordered', 'start_date']},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['user', '-date_added']},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='complete',
            new_name='ordered',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='complete',
            new_name='ordered',
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]