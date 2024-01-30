# Generated by Django 5.0 on 2023-12-18 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_question_true_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_image',
            field=models.ImageField(null=True, upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='question',
            name='True_choice',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=3, verbose_name='true_choice'),
        ),
    ]
