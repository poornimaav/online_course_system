# Generated by Django 4.2.2 on 2023-07-16 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='degree',
        ),
        migrations.RemoveField(
            model_name='student',
            name='major',
        ),
        migrations.RemoveField(
            model_name='student',
            name='university',
        ),
    ]
