# Generated by Django 2.0.2 on 2020-05-05 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0002_auto_20200505_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created_date',
            new_name='created_at',
        ),
    ]
