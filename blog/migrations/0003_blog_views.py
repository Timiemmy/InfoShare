# Generated by Django 5.1.4 on 2024-12-08 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_blog_category_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="views",
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
