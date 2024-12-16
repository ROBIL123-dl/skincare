# Generated by Django 5.1 on 2024-11-29 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('full_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('Role', models.PositiveIntegerField(blank=True, choices=[(2, 'vendor'), (1, 'customer'), (0, 'default')], default=0, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('otp', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('phone_number', models.IntegerField(null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('date_of_join', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_name', models.CharField(max_length=20)),
                ('phone_number', models.BigIntegerField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('status', models.BooleanField(default=False)),
                ('addres', models.TextField(max_length=500)),
                ('license', models.ImageField(upload_to='media/')),
                ('date_of_join', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now_add=True)),
                ('vendor_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
