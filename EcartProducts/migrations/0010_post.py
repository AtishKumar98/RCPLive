# Generated by Django 4.0.3 on 2022-04-11 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcartProducts', '0009_alter_room_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.CharField(max_length=100)),
                ('user_profile', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
        ),
    ]
