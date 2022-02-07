# Generated by Django 3.1.13 on 2022-02-06 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0003_auto_20220105_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinnessNewsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_num', models.IntegerField(unique=True)),
                ('date', models.DateTimeField(null=True)),
                ('title', models.TextField(blank=True, default='', null=True)),
                ('content', models.TextField(blank=True, default='', null=True)),
                ('bull_count', models.IntegerField(blank=True, default=0, null=True)),
                ('bear_count', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]