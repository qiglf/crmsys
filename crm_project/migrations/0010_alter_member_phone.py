# Generated by Django 4.1.5 on 2023-02-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_project', '0009_rename_member_id_member_amount_of_workplaces_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=255, null=True),
        ),
    ]