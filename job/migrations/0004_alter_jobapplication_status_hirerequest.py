# Generated by Django 5.1.3 on 2024-11-13 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_careerhistory_options_and_more'),
        ('job', '0003_remove_jobpost_is_active_alter_jobpost_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Reviewed', 'Reviewed'), ('Shortlisted', 'Shortlisted'), ('Rejected', 'Rejected'), ('Hired', 'Hired')], default='Pending', max_length=20),
        ),
        migrations.CreateModel(
            name='HireRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hire_requests', to='job.jobpost')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hire_requests', to='accounts.jobseeker')),
            ],
            options={
                'unique_together': {('job', 'job_seeker')},
            },
        ),
    ]
