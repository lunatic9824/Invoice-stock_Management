# Generated by Django 3.2.3 on 2021-06-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanagement', '0023_alter_stock_issue_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
