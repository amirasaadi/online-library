# Generated by Django 2.0.6 on 2018-06-25 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reserved', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Copy')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='borrowed_books',
            field=models.ManyToManyField(related_name='a', through='users.Loan', to='book.Copy'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='number_of_donated_books',
            field=models.IntegerField(blank=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customuser',
            name='reserved_books',
            field=models.ManyToManyField(related_name='b', through='users.Reservation', to='book.Copy'),
        ),
    ]
