# Generated by Django 4.0.5 on 2022-06-15 13:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_alter_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='postdate',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='category',
            name='catcolor',
            field=models.CharField(default='red', max_length=100),
        ),
    ]
