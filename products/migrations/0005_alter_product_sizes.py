# Generated by Django 5.1.4 on 2025-02-12 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_sizes_alter_product_parent_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
