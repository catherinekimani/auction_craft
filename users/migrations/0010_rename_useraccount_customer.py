# Generated by Django 4.2.8 on 2023-12-07 16:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_rename_product_auctionitem_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserAccount',
            new_name='Customer',
        ),
    ]