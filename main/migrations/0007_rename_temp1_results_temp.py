# Generated by Django 4.1.7 on 2023-03-09 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_results_temp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='results',
            old_name='temp1',
            new_name='temp',
        ),
    ]
