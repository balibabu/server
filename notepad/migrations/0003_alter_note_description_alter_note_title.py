# Generated by Django 5.0 on 2023-12-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notepad', '0002_note_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]