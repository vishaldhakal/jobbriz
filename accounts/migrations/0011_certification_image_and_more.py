# Generated by Django 5.1.3 on 2024-12-31 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_jobseeker_availability_alter_jobseeker_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='certifications/'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='issuing_organisation',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='certification',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='work_experience',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
