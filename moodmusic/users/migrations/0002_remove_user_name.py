# Generated by Django 3.0.5 on 2020-11-26 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="name",),
    ]
