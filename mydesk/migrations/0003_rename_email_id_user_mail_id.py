# Generated by Django 5.1.3 on 2024-12-09 13:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mydesk", "0002_mailid_alter_user_email_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="email_id",
            new_name="mail_id",
        ),
    ]
