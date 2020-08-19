# Generated by Django 3.0.5 on 2020-08-19 10:14

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+447850306812', max_length=128, region=None, unique=True),
            preserve_default=False,
        ),
    ]