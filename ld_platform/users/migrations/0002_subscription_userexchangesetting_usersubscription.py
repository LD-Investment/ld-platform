# Generated by Django 3.1.13 on 2021-12-01 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0002_auto_20211201_1557'),
        ('bots', '0002_auto_20211201_1557'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bots.bot')),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funds.fund')),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('INAC', 'Inactive'), ('ACTV', 'Active'), ('PAUS', 'Paused'), ('TERM', 'Terminated')], default='INAC', max_length=4)),
                ('run_type', models.CharField(choices=[('BACK', 'Back-testing Mode'), ('SIML', 'Simulation Mode'), ('DRYR', 'Dry-run Mode'), ('LIVR', 'Live-run Mode')], default='LIVR', max_length=4)),
                ('settings', models.JSONField(default=dict)),
                ('subscribe_start_date', models.DateTimeField(null=True)),
                ('subscribe_end_date', models.DateTimeField(null=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserExchangeSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('api_key', models.TextField()),
                ('api_secret', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
