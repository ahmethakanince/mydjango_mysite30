# Generated by Django 5.0 on 2023-12-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0042_alter_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_answer_data',
            name='soru_1',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='student_answer_data',
            name='soru_2',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='student_answer_data',
            name='soru_3',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
