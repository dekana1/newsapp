# Generated by Django 4.1.1 on 2022-09-23 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapi', '0007_alter_hnew_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hnew',
            name='pk_id',
            field=models.IntegerField(verbose_name='HN unique ID'),
        ),
    ]
