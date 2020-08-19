# Generated by Django 3.0.5 on 2020-08-18 15:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=160)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('daily_start', models.TimeField()),
                ('daily_end', models.TimeField()),
                ('surveys_perday', models.IntegerField(verbose_name=django.core.validators.MinValueValidator(1))),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.IntegerField()),
                ('call_sid', models.CharField(max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ema.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ema.Survey'),
        ),
        migrations.CreateModel(
            name='EMAQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happiness', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Happiness')),
                ('energy', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Energy')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ema_questions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('url', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='URL ID')),
                ('valid_until', models.DateTimeField(editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generated_links', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
