# Generated by Django 3.1.3 on 2020-11-08 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performance_register', '0004_auto_20201108_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisorevaluation',
            name='supervisor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='performance_register.supervisor'),
            preserve_default=False,
        ),
    ]
