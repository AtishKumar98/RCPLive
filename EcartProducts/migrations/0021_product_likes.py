# Generated by Django 4.0.3 on 2022-04-17 02:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EcartProducts', '0020_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(related_query_name='Product_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
