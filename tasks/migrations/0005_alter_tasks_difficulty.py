# Generated by Django 5.1.2 on 2024-10-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_tasks_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='difficulty',
            field=models.IntegerField(blank=True, choices=[(10, 'Easy'), (20, 'Medium'), (30, 'Hard')], max_length=255, null=True),
        ),
    ]
