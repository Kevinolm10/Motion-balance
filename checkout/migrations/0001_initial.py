# Generated by Django 5.1.4 on 2025-02-08 21:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('size', models.CharField(blank=True, max_length=10, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(default='C7D32CC3A0E64508B76B1DD124D1F0CB', editable=False, max_length=32, unique=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('shipping_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
