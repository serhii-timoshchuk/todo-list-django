# Generated by Django 4.0.5 on 2022-06-05 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_alter_todo_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='idx',
            field=models.PositiveIntegerField(default=0),
        ),
    ]