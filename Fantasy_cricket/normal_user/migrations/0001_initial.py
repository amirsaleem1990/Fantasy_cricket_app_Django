# Generated by Django 3.2.6 on 2021-11-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team_players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id_in_original_table', models.IntegerField()),
            ],
            options={
                'db_table': 'Team_players',
            },
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.TextField(max_length=20)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'Teams',
            },
        ),
    ]
