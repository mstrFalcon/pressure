# Generated by Django 5.1.2 on 2024-10-31 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pressure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('systolic', models.IntegerField()),
                ('diastolic', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
