# Generated by Django 5.0 on 2024-01-09 08:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0062_number_of_tests_taken_total_extra_time_grade_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptanceofRules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken_acceptance', models.DateTimeField(auto_now_add=True)),
                ('courseid_acceptance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.courses')),
                ('userid_acceptance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
