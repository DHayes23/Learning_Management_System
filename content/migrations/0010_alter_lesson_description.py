# Generated by Django 5.0.7 on 2024-08-22 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_studentprogress_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
