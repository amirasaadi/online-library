from django.db import models
from book.models import Copy
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # initial
    student_id = models.CharField(max_length=8, unique=True, blank=False,null=True)

    # formoula
    number_of_donated_books = models.IntegerField(null=True,blank=True)

    # Profile
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.student_id


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()