# Generated by Django 3.1.3 on 2020-11-08 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('performance_register', '0003_auto_20201108_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supervisorevaluation',
            old_name='date',
            new_name='date_conducted',
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.project')),
            ],
        ),
    ]