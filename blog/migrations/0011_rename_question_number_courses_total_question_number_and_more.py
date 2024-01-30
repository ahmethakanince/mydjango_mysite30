# Generated by Django 5.0 on 2023-12-19 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_rename_question_course_courses_course_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='question_number',
            new_name='total_question_number',
        ),
        migrations.AlterField(
            model_name='courses',
            name='is_active',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='courses',
            name='question_asked',
            field=models.PositiveIntegerField(),
        ),
    ]
