# Generated by Django 3.2.3 on 2021-06-06 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanagement', '0017_product_disc_rs'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.IntegerField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('user_id', models.CharField(max_length=40)),
                ('password_1', models.CharField(max_length=40)),
                ('password_2', models.CharField(max_length=40)),
            ],
        ),
    ]
