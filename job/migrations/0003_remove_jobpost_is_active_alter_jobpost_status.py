# Generated by Django 5.1.3 on 2024-11-13 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_jobapplication_status_jobpost_applications_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpost',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published'), ('Expired', 'Expired'), ('Closed', 'Closed')], default='Published', max_length=20),
        ),
    ]