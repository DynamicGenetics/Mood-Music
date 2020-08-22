# Generated by Django 3.0.5 on 2020-08-22 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ema', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionstate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='emasession',
            name='first_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ema.EMAQuestions'),
        ),
        migrations.AddField(
            model_name='emaresponse',
            name='question',
            field=models.ManyToManyField(related_name='ema_responses', to='ema.EMAQuestions'),
        ),
        migrations.AddField(
            model_name='emaresponse',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ema_responses', to='ema.EMASession'),
        ),
        migrations.AddField(
            model_name='emaresponse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
