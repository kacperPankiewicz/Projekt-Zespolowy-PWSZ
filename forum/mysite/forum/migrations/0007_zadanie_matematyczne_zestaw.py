# Generated by Django 3.0.5 on 2021-04-02 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_zadanie_matematyczne'),
    ]

    operations = [
        migrations.AddField(
            model_name='zadanie_matematyczne',
            name='zestaw',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]