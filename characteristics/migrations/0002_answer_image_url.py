# Generated by Django 4.0.4 on 2022-06-17 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characteristics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='image_url',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
