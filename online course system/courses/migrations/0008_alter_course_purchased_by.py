# Generated by Django 4.2.2 on 2023-07-24 06:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_remove_course_contents_course_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='purchased_by',
            field=models.ManyToManyField(blank=True, related_name='purchased_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
