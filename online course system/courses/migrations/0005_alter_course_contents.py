# Generated by Django 4.2.2 on 2023-07-24 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_student_degree_remove_student_major_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='contents',
            field=models.ManyToManyField(blank=True, null=True, related_name='courses', to='courses.content'),
        ),
    ]
