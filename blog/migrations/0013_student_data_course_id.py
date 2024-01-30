# Generated by Django 5.0 on 2023-12-19 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_student_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_data',
            name='course_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.courses'),
        ),
    ]