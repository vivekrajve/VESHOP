# Generated by Django 5.1b1 on 2024-07-31 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsone', '0002_employee_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='add_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='add_product',
            fields=[
                ('Product_id', models.AutoField(primary_key=True, serialize=False)),
                ('p_name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('image1', models.FileField(upload_to='')),
                ('image2', models.FileField(upload_to='')),
                ('image3', models.FileField(upload_to='')),
                ('image4', models.FileField(upload_to='')),
                ('offer', models.IntegerField()),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total_price', models.IntegerField(default=1)),
                ('product_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.add_product')),
                ('user_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.user_register')),
            ],
        ),
        migrations.CreateModel(
            name='order_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_details', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(default=1)),
                ('total_price', models.IntegerField()),
                ('payment_status', models.CharField(default='NOT PAID', max_length=20)),
                ('delivery_status', models.CharField(default='pending', max_length=20)),
                ('employee_register', models.CharField(default='abc', max_length=20)),
                ('address', models.CharField(default='NIL', max_length=200)),
                ('address_city', models.CharField(max_length=20)),
                ('address_district', models.CharField(max_length=20)),
                ('address_state', models.CharField(max_length=20)),
                ('address_pincode', models.IntegerField(default=0)),
                ('user_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.user_register')),
            ],
        ),
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.add_product')),
                ('user_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.user_register')),
            ],
        ),
    ]
