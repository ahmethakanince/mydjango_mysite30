# Generated by Django 5.0 on 2023-12-19 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_student_data_course_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_data',
            old_name='course_id',
            new_name='course_name',
        ),
    ]
