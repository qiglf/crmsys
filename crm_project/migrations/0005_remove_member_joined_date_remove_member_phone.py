# Generated by Django 4.1.5 on 2023-01-22 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_project', '0004_member_joined_date_member_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='joined_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='phone',
        ),
    ]
