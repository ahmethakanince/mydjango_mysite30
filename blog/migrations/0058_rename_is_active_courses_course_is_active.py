# Generated by Django 5.0 on 2023-12-29 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0057_alter_courses_devolement_mode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='is_active',
            new_name='course_is_active',
        ),
    ]
