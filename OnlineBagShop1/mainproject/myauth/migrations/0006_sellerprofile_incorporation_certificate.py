# Generated by Django 4.2.5 on 2023-11-11 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0005_alter_profile_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerprofile',
            name='incorporation_certificate',
            field=models.FileField(blank=True, null=True, upload_to='incorporation_certificates/'),
        ),
    ]
