# Generated by Django 5.1.3 on 2024-11-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_alter_jobapplication_status_hirerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='hirerequest',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]