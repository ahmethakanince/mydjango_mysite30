# Generated by Django 5.0 on 2023-12-22 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0049_rename_course_number_of_tests_taken_course_tested_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='number_of_tests_taken',
            old_name='course_tested',
            new_name='courseid_tested',
        ),
        migrations.RenameField(
            model_name='number_of_tests_taken',
            old_name='user_tested',
            new_name='userid_tested',
        ),
    ]