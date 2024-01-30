# Generated by Django 5.0 on 2023-12-21 18:50

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_alter_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='A',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='A'),
        ),
        migrations.AlterField(
            model_name='question',
            name='B',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='B'),
        ),
        migrations.AlterField(
            model_name='question',
            name='C',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='C'),
        ),
        migrations.AlterField(
            model_name='question',
            name='D',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='D'),
        ),
        migrations.AlterField(
            model_name='question',
            name='E',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='E'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
