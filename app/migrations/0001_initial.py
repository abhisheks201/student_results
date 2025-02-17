# Generated by Django 4.1.7 on 2023-07-07 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('hall_ticket', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('school', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telugu', models.CharField(max_length=50)),
                ('hindi', models.CharField(max_length=50)),
                ('english', models.CharField(max_length=100)),
                ('maths', models.CharField(max_length=50)),
                ('science', models.CharField(max_length=100)),
                ('social', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='app.user')),
            ],
            options={
                'db_table': 'Marks',
            },
        ),
    ]
