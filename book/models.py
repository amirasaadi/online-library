from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

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

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return '{}- {}'.format(self.id,self.book)


class Loan(models.Model):

    # link
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Copy,on_delete=models.CASCADE)

    # initial
    date_due = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.person,self.book,self.date_due)

class Reservation(models.Model):

    # link
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Copy, on_delete=models.CASCADE)

    # initial
    date_reserved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.person,self.book,self.date_reserved)


@receiver(post_save, sender=Book)
def send_newbook_email(sender,instance,created,**kwargs):
    if created:
        subject = 'New book aded to library'
        message = 'Hi {name}!\n\tWe adad this book to our library, you can Borrow or Reserve it!\n\t{book}'.format(name='ali',book=instance)
        # users = list(User.objects.all())
        # recipient_list =[]
        # for user in users:
        #     recipient_list.append(user.email)
        recipient_list = ["paul@polo.com"]
        from_email = ['book@book.ir']
        # send_mail(subject,message,recipient_list)
        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)

@receiver(post_delete,sender=Book)
def send_bookdeleted_email(sender,instance,**kwargs):
    subject = 'Some book deleted'
    message = 'Hi {name}!\n\tWe removed this book from our library, you can\'t Borrow or Reserve it any more!\n\t{book}'.format(name='ali', book=instance)
    # users = list(User.objects.all())
    # recipient_list = []
    # for user in users:
    #     recipient_list.append(user.email)
    # names_list =[]
    # for user in users:
    #     names_list = user.first_name
    recipient_list = ["paul@polo.com"]
    from_email = ['book@book.ir']
    # for i in range(len(users)):
    #     message = 'Hi {name}!\n\tWe removed this book from our library, you can\'t Borrow or Reserve it any more!\n\t{book}'.format(
    #         name=names_list[i], book=instance)
    #     send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list[i])
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)