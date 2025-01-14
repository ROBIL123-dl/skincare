# Generated by Django 5.1 on 2024-12-29 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0016_alter_payment_payment_category'),
        ('user_management', '0022_coupon_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.customer_profile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.vendor_profile')),
            ],
        ),
    ]
