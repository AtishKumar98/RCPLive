# Generated by Django 3.2.15 on 2022-09-24 07:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EcartProducts', '0034_refund_order_refund'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='blog', to=settings.AUTH_USER_MODEL),
        ),
    ]
