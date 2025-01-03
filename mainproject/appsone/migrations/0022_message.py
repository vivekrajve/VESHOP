# Generated by Django 3.0 on 2024-10-21 07:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appsone', '0021_paid_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('reply', models.TextField(default='We will get back to you..')),
                ('status', models.TextField(default='0')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.UserRegister1')),
            ],
        ),
    ]
