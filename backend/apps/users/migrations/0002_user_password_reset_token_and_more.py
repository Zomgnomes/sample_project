# Generated by Django 4.1.7 on 2023-02-17 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password_token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]