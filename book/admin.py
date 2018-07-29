from django.contrib import admin
from book import models


admin.site.register(models.Author)
admin.site.register(models.Translator)
admin.site.register(models.Publisher)

admin.site.register(models.Loan)
admin.site.register(models.Book)
admin.site.register(models.Copy)


def reserve_to_return_Back(modeladmin,request,queryset):
    for item in queryset:
        person = item.person
        book = item.book
        item.delete()
        models.Copy.objects.filter(id=book.id).update(status='a')


def reserve_to_loan(modeladmin,request,queryset):

    for item in queryset:
        person = item.person
        book = item.book
        models.Loan(person=person, book=book).save()
        item.delete()
        models.Copy.objects.filter(id=book.id).update(status='o')


class Reservations_Admin(admin.ModelAdmin):
    list_display = ('person','book','date_reserved')
    actions = [reserve_to_loan,reserve_to_return_Back]

admin.site.register(models.Reservation,Reservations_Admin)