# Generated by Django 2.2.5 on 2020-07-01 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20200701_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Accuracy',
            new_name='accuracy',
        ),
    ]