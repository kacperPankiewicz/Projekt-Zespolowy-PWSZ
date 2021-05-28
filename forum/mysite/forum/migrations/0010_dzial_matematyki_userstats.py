# Generated by Django 3.0.5 on 2021-05-28 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20210504_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dzial_matematyki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dzial', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometria', models.CharField(max_length=50)),
                ('trygonometria', models.CharField(max_length=50)),
                ('logarytmy', models.CharField(max_length=50)),
                ('potegowanie', models.CharField(max_length=50)),
                ('pierwiastkowanie', models.CharField(max_length=50)),
                ('funkcje', models.CharField(max_length=50)),
                ('prawdopodobienstwo', models.CharField(max_length=50)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.User')),
            ],
        ),
    ]
