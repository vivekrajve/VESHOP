# Generated by Django 3.0 on 2024-08-09 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appsone', '0004_rename_description_add_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, null=True, upload_to='path/to/upload')),
                ('offer', models.IntegerField()),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.product'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='product_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsone.product'),
        ),
        migrations.DeleteModel(
            name='add_product',
        ),
    ]
