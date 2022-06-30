# Generated by Django 4.0.3 on 2022-04-16 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcartProducts', '0016_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Complete', 'Complete'), ('Failed', 'Failed'), ('Cancelled', 'Cancelled')], max_length=100, null=True),
        ),
    ]
