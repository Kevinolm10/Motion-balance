# Generated by Django 5.1.4 on 2025-01-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_created_at_remove_product_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='nav_element',
            field=models.CharField(choices=[('products', 'Products'), ('accessories', 'Accessories'), ('sale', 'Sale')], default='products', max_length=20),
        ),
    ]
