# Generated by Django 4.0.3 on 2022-04-17 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcartProducts', '0022_orderitem_checksum_orderitem_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Complete', 'Complete'), ('Failed', 'Failed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100, null=True),
        ),
    ]
