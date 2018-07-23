from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from datetime import datetime,timedelta
from book import constants

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

    POEM = 'P'
    STORY = 'S'
    HISTORY = 'H'
    MAGAZINE = 'M'
    BIOGRAPHU = 'B'
    subject_choices = (
        (POEM, 'Poem'),
        (STORY, 'Story'),
        (HISTORY, 'History'),
        (MAGAZINE, 'Magazine'),
        (BIOGRAPHU,'Biography'),
    )
    subject = models.CharField(
        max_length=1,
        choices=subject_choices,
        default=STORY,
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

    # test moving query views to here
    def students_who_do_not_loan_any():
        result = User.objects.exclude(id__in=Loan.objects.values('person__id'))
        context = {'students': result}
        return context

    def books_loned_between_two_times(start_date,end_date):
        books = Loan.objects.filter(date_due__range=[start_date, end_date])
        # return super().form_valid(form)
        # to do its better to change it to render
        context = {'context': books}
        return context

    def authors_loaned_by_student(username):
        user_loans = Loan.objects.filter(person__username__exact=username)
        # Loan.objects.filter(person__icontain)
        result = user_loans.values_list('book__book__authors__name', flat=True)
        context = {'context': result}
        return context

    def loan_near_due_date():
        context = {}
        queryset = Loan.objects.filter(
            date_due__lt=datetime.now().date() - timedelta(days=constants.LOAN_TIME - constants.NEAR))
        context['context'] = queryset
        return context

    def students_who_borrow_books_in_special_publish_year(year):
        book_published_in_year = Loan.objects.filter(book__book__publish_year__exact=year)
        result = book_published_in_year.values_list('person__username', flat=True)
        context = {'context': result}
        return context

class Copy(models.Model):
    # link
    borrowers = models.ManyToManyField(User, through='Loan', related_name='a')
    reservers = models.ManyToManyField(User, through='Reservation', related_name='b')

    book = models.ForeignKey(Book, on_delete=models.CASCADE)


    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')


    def __str__(self):
        return '{}- {}'.format(self.id,self.book)


class Loan(models.Model):

    # link
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Copy,on_delete=models.CASCADE)

    # initial
    #start
    date_due = models.DateField(auto_now_add=True)
    #end
    due_back = models.DateField(null=True, blank=True)

    def can_loan(self):
        firstone = Reservation.objects.filter(book=self.book)[0]
        if firstone.person == self.person:
            return True
        else:
            return False

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
        messages = []
        subject = 'New book aded to library'
        message = """Hi dear students!
                    \n\tWe adad this book to our library, you can Borrow or Reserve it!
                    \n\t{book}""".format(book=instance)

        emails = User.objects.values_list('email', flat=True)
        recipient_list = list(emails)

        from_email = ['book@book.ir']

        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)

@receiver(post_delete,sender=Book)
def send_bookdeleted_email(sender,instance,**kwargs):
    subject = 'Some book deleted'
    message = """Hi dear students!
                \n\tWe removed this book from our library, you can\'t Borrow or Reserve it any more!
                \n\t{book}""".format(book=instance)

    emails = User.objects.values_list('email', flat=True)
    recipient_list = list(emails)

    from_email = ['book@book.ir']

    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)