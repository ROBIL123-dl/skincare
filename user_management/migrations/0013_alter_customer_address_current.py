# Generated by Django 5.1 on 2024-12-05 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0012_alter_customer_address_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_address',
            name='current',
            field=models.BooleanField(blank=True, choices=[(True, 'current address'), (False, 'not current address')], default=False),
        ),
    ]
