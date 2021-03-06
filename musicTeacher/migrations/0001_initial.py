# Generated by Django 2.1.1 on 2018-09-09 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('upd_date', models.DateTimeField(verbose_name='date updated')),
                ('sheets_folder', models.CharField(max_length=400)),
                ('is_original', models.BooleanField(default=True)),
                ('audio', models.CharField(max_length=400)),
            ],
        ),
    ]
