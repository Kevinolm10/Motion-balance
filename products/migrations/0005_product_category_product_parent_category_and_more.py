# Generated by Django 5.1.4 on 2025-02-04 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='parent_category',
            field=models.CharField(choices=[('products', 'Products'), ('accessories', 'Accessories'), ('sale', 'Sale')], default='products', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory_name',
            field=models.CharField(default='Miscellaneous', max_length=255),
            preserve_default=False,
        ),
    ]
