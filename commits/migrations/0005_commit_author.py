# Generated by Django 5.0.1 on 2024-01-18 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commits', '0004_remove_commit_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='author',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
