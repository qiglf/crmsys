# Generated by Django 4.1.7 on 2023-03-08 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_project', '0011_alter_work_years'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='sphere',
        ),
        migrations.AddField(
            model_name='work',
            name='level',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='reference',
            field=models.BooleanField(null=True),
        ),
    ]
