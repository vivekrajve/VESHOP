# Generated by Django 3.0 on 2024-08-27 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appsone', '0009_auto_20240824_1116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopemployeeregister',
            old_name='user_name',
            new_name='employee_name',
        ),
    ]
