# Generated by Django 5.1.3 on 2024-12-17 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_user_type'),
        ('job', '0006_hirerequest_seeker_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprenticeshipCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Apprenticeship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('level', models.CharField(choices=[('Level 1', 'Level 1'), ('Level 2', 'Level 2'), ('Level 3', 'Level 3'), ('Level 4', 'Level 4'), ('Level 5', 'Level 5'), ('Level 6', 'Level 6'), ('Level 7', 'Level 7'), ('Level 8', 'Level 8'), ('None', 'None')], default='None', max_length=20)),
                ('overview_of_role', models.TextField()),
                ('duration', models.CharField(choices=[('6 months', '6 months'), ('12 months', '12 months'), ('18 months', '18 months'), ('24 months', '24 months'), ('30 months', '30 months'), ('36 months', '36 months'), ('None', 'None')], default='None', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('occupation_summary', models.TextField()),
                ('occupation_description', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apprenticeships_created', to='accounts.company')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apprenticeships', to='job.apprenticeshipcategory')),
            ],
        ),
    ]
