# Generated by Django 5.0 on 2024-02-29 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunk',
            name='size',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
    ]
