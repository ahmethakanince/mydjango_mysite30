# Generated by Django 5.0 on 2023-12-22 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0039_alter_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='total_question_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
