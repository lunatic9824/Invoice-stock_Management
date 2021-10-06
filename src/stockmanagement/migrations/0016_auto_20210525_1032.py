# Generated by Django 3.2.3 on 2021-05-25 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanagement', '0015_remove_invoice_details_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice_details',
            name='Invoice_num',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='Cgst',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Discount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Igst',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Sgst',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]