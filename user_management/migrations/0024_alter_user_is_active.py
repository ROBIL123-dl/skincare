# Generated by Django 5.1 on 2025-01-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0023_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
