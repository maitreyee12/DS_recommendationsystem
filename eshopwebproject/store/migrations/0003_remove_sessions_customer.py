# Generated by Django 4.2.2 on 2023-08-16 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_sessions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sessions",
            name="customer",
        ),
    ]
