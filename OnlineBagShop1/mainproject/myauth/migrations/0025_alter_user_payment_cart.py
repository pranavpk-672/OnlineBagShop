# Generated by Django 4.2.5 on 2023-12-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0024_alter_user_payment_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_payment',
            name='cart',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]