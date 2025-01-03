# Generated by Django 5.1.3 on 2024-11-09 06:41

import django.db.models.deletion
import job.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MajorGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
            bases=(job.models.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SubMajorGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField()),
                ('major_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_major_groups', to='job.majorgroup')),
            ],
            bases=(job.models.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MinorGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField()),
                ('sub_major_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minor_groups', to='job.submajorgroup')),
            ],
            bases=(job.models.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UnitGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField()),
                ('minor_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_groups', to='job.minorgroup')),
            ],
            bases=(job.models.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('required_skill_level', models.CharField(choices=[('RPL', 'RPL'), ('Level 1', 'Level 1'), ('Level 2', 'Level 2'), ('Level 3', 'Level 3'), ('Level 4', 'Level 4'), ('Level 5', 'Level 5'), ('Level 6', 'Level 6'), ('Level 7', 'Level 7'), ('Level 8', 'Level 8'), ('None', 'None')], default='None', max_length=10)),
                ('required_education', models.CharField(choices=[('General Literate', 'General Literate'), ('Below SLC', 'Below SLC'), ('+2', '+2'), ('Bachelors', 'Bachelors'), ('Master & above', 'Master & above'), ('Pre-Diploma', 'Pre-Diploma'), ('Diploma', 'Diploma'), ('TLSC', 'TLSC'), ('No Education', 'No Education')], default='No Education', max_length=20)),
                ('description', models.TextField()),
                ('responsibilities', models.TextField()),
                ('requirements', models.TextField()),
                ('salary_range_min', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_range_max', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('employment_type', models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Contract', 'Contract'), ('Internship', 'Internship')], max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company')),
                ('location', models.ManyToManyField(related_name='job_posts', to='accounts.location')),
                ('unit_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.unitgroup')),
            ],
            bases=(job.models.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_date', models.DateTimeField(auto_now_add=True)),
                ('cover_letter', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.jobseeker')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobpost')),
            ],
            options={
                'unique_together': {('job', 'applicant')},
            },
        ),
        migrations.CreateModel(
            name='SavedJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_date', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobpost')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.jobseeker')),
            ],
            options={
                'unique_together': {('job', 'job_seeker')},
            },
        ),
    ]
