# Generated by Django 3.2.6 on 2021-11-04 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='recorded',
            field=models.IntegerField(default=0),
        ),
    ]