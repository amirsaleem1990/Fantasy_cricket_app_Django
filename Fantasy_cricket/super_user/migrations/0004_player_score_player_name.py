# Generated by Django 3.2.6 on 2021-11-05 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_user', '0003_player_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_score',
            name='player_name',
            field=models.TextField(default='p', max_length=40),
            preserve_default=False,
        ),
    ]