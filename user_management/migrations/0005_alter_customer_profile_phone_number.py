# Generated by Django 5.1 on 2024-12-03 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_alter_customer_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_profile',
            name='phone_number',
            field=models.BigIntegerField(null=True),
        ),
    ]
