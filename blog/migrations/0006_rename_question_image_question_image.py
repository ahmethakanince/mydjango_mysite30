# Generated by Django 5.0 on 2023-12-18 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_question_question_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_image',
            new_name='image',
        ),
    ]