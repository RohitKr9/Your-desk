# Generated by Django 5.1.3 on 2024-12-05 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mydesk", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MailId",
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
                ("mail_id", models.EmailField(max_length=254)),
                ("otp", models.IntegerField(null=True)),
            ],
            options={
                "db_table": "mail_id",
            },
        ),
        migrations.AlterField(
            model_name="user",
            name="email_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="mydesk.mailid"
            ),
        ),
    ]