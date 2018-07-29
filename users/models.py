from django.db import models
from book.models import Loan,Copy
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from book import constants

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # initial
    student_id = models.CharField(max_length=8, unique=True, blank=True,null=True)

    # formoula
    number_of_donated_books = models.IntegerField(default=0, null=True,blank=True)
    penalty = models.IntegerField(default=0,null=True,blank=True)

    # Profile
    image = models.ImageField(blank=True,upload_to='profile_image')

    # def __str__(self):
    #     return self.student_id

    def best_students():
        students = User.objects.all()
        for student in students:
            student_loans = Loan.objects.filter(person=student)
            penalty = 0
            for loan in student_loans:
                delta = loan.due_back - loan.date_due
                if delta > constants.LOAN_TIME:
                    penalty += delta
        pass



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
