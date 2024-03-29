# Generated by Django 3.1.13 on 2022-05-15 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0006_delete_coinnessnewsdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bot',
            name='version',
        ),
        migrations.AlterField(
            model_name='bot',
            name='name',
            field=models.CharField(choices=[('news-tracker', 'News Tracker')], max_length=256),
        ),
        migrations.AlterField(
            model_name='bot',
            name='type',
            field=models.CharField(choices=[('automated-bot', 'Automated Bot'), ('manual-bot', 'Manual Bot'), ('indicator-bot', 'Indicator Bot')], default='automated-bot', max_length=256),
        ),
        migrations.AlterField(
            model_name='subscribedbot',
            name='run_type',
            field=models.CharField(choices=[('back-test', 'Back-testing Mode'), ('simulation', 'Simulation Mode'), ('dry-run', 'Dry-run Mode'), ('live-run', 'Live-run Mode')], default='live-run', max_length=256),
        ),
        migrations.AlterField(
            model_name='subscribedbot',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive', max_length=256),
        ),
    ]
