# Generated by Django 5.1.3 on 2024-11-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_careerhistory_options_and_more'),
        ('job', '0004_alter_jobapplication_status_hirerequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='certifications',
            field=models.ManyToManyField(blank=True, related_name='job_seeker_certifications', to='accounts.certification'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='job_seeker_languages', to='accounts.language'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='preferred_locations',
            field=models.ManyToManyField(blank=True, related_name='job_seeker_preferred_locations', to='accounts.location'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='preferred_unit_groups',
            field=models.ManyToManyField(blank=True, related_name='job_seeker_preferred_unit_groups', to='job.unitgroup'),
        ),
    ]