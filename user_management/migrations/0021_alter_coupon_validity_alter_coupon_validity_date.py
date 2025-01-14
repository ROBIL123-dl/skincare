# Generated by Django 5.1 on 2024-12-20 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0020_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='validity',
            field=models.DateTimeField(null=True, verbose_name='Validity'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='validity_date',
            field=models.IntegerField(),
        ),
    ]
