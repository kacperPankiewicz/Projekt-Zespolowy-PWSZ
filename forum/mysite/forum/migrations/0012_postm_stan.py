# Generated by Django 3.0.5 on 2021-04-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20210407_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='postm',
            name='stan',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]