# Generated by Django 4.0.5 on 2022-06-15 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.FileField(default='default.jpg', upload_to=''),
        ),
    ]
