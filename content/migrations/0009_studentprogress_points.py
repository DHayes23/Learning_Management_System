# Generated by Django 5.0.7 on 2024-08-17 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_question_lesson_difficulty_lesson_due_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprogress',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
