# Generated by Django 5.1.3 on 2024-12-17 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_apprenticeshipcategory_apprenticeship'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apprenticeshipcategory',
            old_name='name',
            new_name='title',
        ),
    ]
