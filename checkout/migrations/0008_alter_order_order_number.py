# Generated by Django 5.1.4 on 2025-02-12 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='3A16AC9289384E6496FE6D4A37237163', editable=False, max_length=32, unique=True),
        ),
    ]
