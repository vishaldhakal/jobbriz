# Generated by Django 5.1.3 on 2024-11-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='industry',
            options={'verbose_name_plural': 'Industries'},
        ),
        migrations.AddField(
            model_name='industry',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]