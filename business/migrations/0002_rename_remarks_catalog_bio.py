# Generated by Django 3.2.19 on 2024-01-27 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='catalog',
            old_name='remarks',
            new_name='bio',
        ),
    ]
