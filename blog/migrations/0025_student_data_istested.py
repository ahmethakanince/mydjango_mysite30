# Generated by Django 5.0 on 2023-12-19 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_alter_question_a_alter_question_b_alter_question_c_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_data',
            name='istested',
            field=models.BooleanField(default=False),
        ),
    ]
