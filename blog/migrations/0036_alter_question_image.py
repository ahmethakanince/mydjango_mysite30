# Generated by Django 5.0 on 2023-12-21 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_alter_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, upload_to='blogs'),
        ),
    ]
