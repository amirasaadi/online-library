# Generated by Django 2.0.6 on 2018-07-06 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180630_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='student_id',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
    ]