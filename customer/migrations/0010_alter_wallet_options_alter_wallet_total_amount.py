# Generated by Django 5.1 on 2024-12-27 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_wallet'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='wallet',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, help_text='The total price of the order.', max_digits=10, verbose_name='Total Amount'),
        ),
    ]
