from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Translator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """ books of the library"""

    name = models.CharField(max_length=255)
    publish_year = models.DateField()
    ISBN = models.BigIntegerField()
    subject = (
        ('p', 'Poem'),
        ('s', 'Story'),
        ('h', 'History'),
        ('m', 'Magazine'),
        ('b', 'Biography'),
    )
    translators = models.ManyToManyField(Translator, blank=True)
    authors = models.ManyToManyField(Author)
    publishers = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    class Meta:
        # this ordering makes time issue
        ordering = ["-name"]

    def get_absolute_url(self):
        return reverse('book:detail_book', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Copy(models.Model):
    # link
    borrowers = models.ManyToManyField(User, through='Loan', related_name='a')
    reservers = models.ManyToManyField(User, through='Reservation', related_name='b')

    book = models.OneToOneField(Book, on_delete=models.CASCADE)


class Loan(models.Model):

    # link
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Copy,on_delete=models.CASCADE)

    # initial
    date_due = models.DateField(auto_now_add=True)


class Reservation(models.Model):

    # link
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Copy, on_delete=models.CASCADE)

    # initial
    date_reserved = models.DateTimeField(auto_now_add=True)