# Generated by Django 3.2.15 on 2022-10-30 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcartProducts', '0035_alter_product_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='multiple_image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
