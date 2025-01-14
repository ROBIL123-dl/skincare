# Generated by Django 5.1 on 2024-12-27 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_alter_order_coupon_price'),
        ('user_management', '0022_coupon_quantity'),
        ('vendor', '0007_alter_products_offer_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.customer_profile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.products', verbose_name='')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.vendor_profile', verbose_name='vendor')),
            ],
        ),
    ]
