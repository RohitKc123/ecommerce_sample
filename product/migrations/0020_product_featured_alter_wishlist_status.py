# Generated by Django 4.1.4 on 2023-01-10 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_wishlist_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Review', 'In Review'), ('Canceled', 'Canceled'), ('Completed', 'Completed')], default='Pending', max_length=15),
        ),
    ]
