# Generated by Django 4.1.4 on 2022-12-30 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_delete_stock_product_company_product_generation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('SOLD', 'SOLD'), ('IN_STOCK', 'IN_STOCK')], default='IN_STOCK', max_length=10),
        ),
    ]