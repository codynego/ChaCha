# Generated by Django 4.2.6 on 2023-10-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0005_remove_user_review_remove_user_verified_user_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
