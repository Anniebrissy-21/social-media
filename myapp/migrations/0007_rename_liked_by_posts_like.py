# Generated by Django 4.2.6 on 2024-02-14 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_comments_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='liked_by',
            new_name='like',
        ),
    ]
