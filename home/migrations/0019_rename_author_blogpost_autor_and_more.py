# Generated by Django 5.1.1 on 2024-10-01 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_blogpost_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='author',
            new_name='autor',
        ),
        migrations.RenameField(
            model_name='blogpost',
            old_name='content',
            new_name='contenido',
        ),
        migrations.RenameField(
            model_name='blogpost',
            old_name='slug',
            new_name='subtítulo',
        ),
        migrations.RenameField(
            model_name='blogpost',
            old_name='title',
            new_name='título',
        ),
    ]
