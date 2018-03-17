# Generated by Django 2.0.3 on 2018-03-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatPer3600Minutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_date', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
                ('relation_id', models.IntegerField()),
                ('additional_field', models.IntegerField()),
            ],
            options={
                'db_table': 'stat_per_3600_minutes',
            },
        ),
    ]