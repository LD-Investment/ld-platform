# Generated by Django 3.1.13 on 2022-02-07 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_coinnessnewsdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coinnessnewsdata',
            name='bear_count',
        ),
        migrations.RemoveField(
            model_name='coinnessnewsdata',
            name='bull_count',
        ),
    ]
