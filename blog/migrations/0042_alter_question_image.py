# Generated by Django 5.0 on 2023-12-22 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_remove_student_answer_data_soru_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogs'),
        ),
    ]