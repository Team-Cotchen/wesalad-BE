# Generated by Django 4.0.4 on 2022-06-28 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_place_postplace'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyway',
            name='description',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(default='active', max_length=50),
        ),
    ]