# Generated by Django 3.1.3 on 2020-11-11 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_userprofile__active_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='_active_project',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]
