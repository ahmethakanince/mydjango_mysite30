# Generated by Django 5.0 on 2023-12-22 12:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0045_student_answer_data_soru_1_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
