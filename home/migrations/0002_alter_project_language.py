# Generated by Django 4.0.3 on 2022-04-28 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="language",
            field=models.CharField(max_length=10),
        ),
    ]
