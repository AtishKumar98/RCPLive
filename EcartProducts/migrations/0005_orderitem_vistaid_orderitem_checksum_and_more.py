# Generated by Django 4.0.3 on 2022-04-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcartProducts', '0004_customer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='VISTAid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='checksum',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='complete',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
    ]
