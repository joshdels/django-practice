# Generated by Django 5.2.4 on 2025-07-19 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=100)),
                ("firstname", models.CharField(max_length=100)),
                ("lastname", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=200)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
