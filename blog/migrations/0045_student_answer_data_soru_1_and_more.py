# Generated by Django 5.0 on 2023-12-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_remove_student_answer_data_soru_1_and_more'),
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
