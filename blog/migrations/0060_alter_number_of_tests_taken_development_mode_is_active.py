# Generated by Django 5.0 on 2023-12-29 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0059_number_of_tests_taken_development_mode_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number_of_tests_taken',
            name='development_mode_is_active',
            field=models.BooleanField(),
        ),
    ]
