# Generated by Django 4.1.1 on 2022-09-25 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapi', '0009_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='type',
            field=models.CharField(choices=[('story', 'story'), ('job', 'job'), ('comment', 'comment'), ('poll', 'poll'), ('pollopt', 'pollopt')], default=3, max_length=10, verbose_name='article type'),
        ),
        migrations.AlterField(
            model_name='hnew',
            name='type',
            field=models.CharField(choices=[('story', 'story'), ('job', 'job'), ('comment', 'comment'), ('poll', 'poll'), ('pollopt', 'pollopt')], default=1, max_length=10, verbose_name='article type'),
        ),
        migrations.AlterField(
            model_name='ournews',
            name='type',
            field=models.CharField(choices=[('story', 'story'), ('job', 'job'), ('comment', 'comment'), ('poll', 'poll'), ('pollopt', 'pollopt')], default='story', max_length=10, verbose_name='article type'),
        ),
    ]
