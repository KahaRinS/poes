# Generated by Django 4.1.7 on 2023-03-09 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_results_temp1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='temp',
        ),
    ]
