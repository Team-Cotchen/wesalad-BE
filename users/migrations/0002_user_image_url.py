# Generated by Django 4.0.4 on 2022-06-10 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image_url',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
