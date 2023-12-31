# Generated by Django 4.2.5 on 2023-10-08 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя работника')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия работника')),
                ('likes', models.IntegerField(verbose_name='Лайки')),
                ('dislikes', models.IntegerField(verbose_name='Дизлайки')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер стола')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.worker', verbose_name='Работник')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
