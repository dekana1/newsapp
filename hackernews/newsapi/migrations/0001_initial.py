# Generated by Django 4.1.1 on 2022-09-19 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OurNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='News Score')),
                ('time_created', models.DateTimeField(auto_now=True, verbose_name='time created')),
                ('title', models.CharField(max_length=50, verbose_name='article title')),
                ('type', models.CharField(choices=[('1', 'job'), ('2', 'comment'), ('3', 'poll'), ('4', 'pollopt')], default=1, max_length=10, verbose_name='article type')),
                ('content', models.CharField(max_length=50, verbose_name='article content')),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
        ),
    ]
