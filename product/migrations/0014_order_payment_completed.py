# Generated by Django 4.1.4 on 2023-01-09 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]