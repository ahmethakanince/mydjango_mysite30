# Generated by Django 5.0 on 2023-12-19 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_student_data_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_data',
            name='student_email',
        ),
        migrations.RemoveField(
            model_name='student_data',
            name='student_name',
        ),
    ]
