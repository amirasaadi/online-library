# Generated by Django 2.0.6 on 2018-06-28 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180628_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='student_id',
            field=models.CharField(max_length=8, null=True, unique=True),
        ),
    ]
