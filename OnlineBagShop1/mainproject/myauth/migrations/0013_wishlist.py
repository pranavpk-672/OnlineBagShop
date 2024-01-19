# Generated by Django 4.2.5 on 2023-11-16 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0012_cart_cart_verify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myauth.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]