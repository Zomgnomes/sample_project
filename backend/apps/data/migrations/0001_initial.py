# Generated by Django 4.2.2 on 2023-06-30 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleDataDaily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('red', models.IntegerField()),
                ('green', models.IntegerField()),
                ('blue', models.IntegerField()),
                ('nir', models.IntegerField()),
                ('related_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Example Data Daily',
                'verbose_name_plural': 'Example Data Daily',
                'ordering': ['related_id', 'date'],
            },
        ),
    ]