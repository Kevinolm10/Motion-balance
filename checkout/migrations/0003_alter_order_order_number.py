# Generated by Django 5.1.4 on 2025-02-10 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='BE5B31EABA904203B48CBB1B50BA442D', editable=False, max_length=32, unique=True),
        ),
    ]
