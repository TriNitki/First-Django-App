# Generated by Django 4.1.1 on 2022-11-03 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0004_entry_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='owner',
        ),
    ]
