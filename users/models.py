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
    score = models.IntegerField(default=0,null=True,blank=True)
    # Profile
    image = models.ImageField(blank=True,upload_to='profile_image')

    def calculate_score(self):

        penalty = self.penalty
        donate = self.number_of_donated_books
        loan = Loan.objects.filter(person=self.user).count()
        self.score =  (penalty*3 - donate*4 + loan *2)
        Profile.objects.filter(id=self.id).update(score = self.score)

    # @property
    # def score(self):
    #     penalty = self.penalty
    #     donate = self.number_of_donated_books
    #     loan = Loan.objects.count(person=self.user)
    #     return (penalty*3 - donate*4 + loan *2)

    # def __str__(self):
    #     return self.student_id

    # def best_students():
    #     students = User.objects.all()
    #     for student in students:
    #         penalty = student.profile.penalty
    #         donate = student.profile.number_of_donated_books
    #         loan = Loan.objects.count(person=student)
    #         score = (penalty*3 - donate*4 + loan *2)
    #
    #     pass
    def best_students(self):

        students = Profile.objects.all()
        for student in students:
            student.calculate_score()
        # print('hello from best_students method')
        return Profile.objects.all().order_by('-score')



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
