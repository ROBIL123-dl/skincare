# Generated by Django 5.1 on 2024-12-28 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Shipping', 'Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Return', 'Return'), ('Returned', 'Returned')], default='Pending', help_text='The current status of the order.', max_length=20, verbose_name='Order Status'),
        ),
    ]
