# Generated by Django 4.2 on 2023-12-10 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KitchenKeepOnSwitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]