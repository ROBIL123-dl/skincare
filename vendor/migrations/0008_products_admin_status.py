# Generated by Django 5.1 on 2025-01-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_alter_products_offer_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='admin_status',
            field=models.BooleanField(default=True),
        ),
    ]
