# Generated by Django 3.0 on 2024-10-15 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsone', '0020_remove_paid_product_cart_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='paid_product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]