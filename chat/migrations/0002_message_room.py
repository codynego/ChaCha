# Generated by Django 4.2.6 on 2023-10-28 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]