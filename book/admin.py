from django.contrib import admin
from book import models
# Register your models here.

admin.site.register(models.Author)
admin.site.register(models.Translator)
admin.site.register(models.Publisher)