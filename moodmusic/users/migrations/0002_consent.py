# Generated by Django 3.0.5 on 2020-10-13 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen_information', models.BooleanField(default=False)),
                ('voluntary_participation', models.BooleanField(default=False)),
                ('data_unwithdrawable', models.BooleanField(default=False)),
                ('data_collected', models.BooleanField(default=False)),
                ('confidentiality', models.BooleanField(default=False)),
                ('data_access', models.BooleanField(default=False)),
                ('data_stored_longterm', models.BooleanField(default=False)),
                ('could_be_reused', models.BooleanField(default=False)),
                ('breaking_confidentiality', models.BooleanField(default=False)),
                ('full_consent', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
