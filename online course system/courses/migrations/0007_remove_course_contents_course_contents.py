# Generated by Django 4.2.2 on 2023-07-24 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_remove_course_contents_course_contents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='contents',
        ),
        migrations.AddField(
            model_name='course',
            name='contents',
            field=models.ManyToManyField(blank=True, null=True, related_name='courses', to='courses.content'),
        ),
    ]
