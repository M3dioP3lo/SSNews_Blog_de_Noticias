# Generated by Django 5.1.1 on 2024-10-10 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_blog_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='categoria',
            field=models.CharField(choices=[('politica', 'Política'), ('deportes', 'Deportes'), ('internacionales', 'Internacionales'), ('ciencia', 'Ciencia')], default='politica', max_length=20),
        ),
    ]
