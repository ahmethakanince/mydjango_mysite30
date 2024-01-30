# Generated by Django 5.0 on 2023-12-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0061_rename_devolement_mode_courses_development_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='number_of_tests_taken',
            name='Total_extra_time_grade',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='number_of_tests_taken',
            name='Total_grade',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='number_of_tests_taken',
            name='Total_theta_grade',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='number_of_tests_taken',
            name='ability_theta',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
    ]
