from datetime import datetime,timedelta

from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from book import models as book_models
from book import forms as book_forms

from django.contrib.auth.models import User

# ip blocking
from ratelimit.mixins import RatelimitMixin
from book import constants

class CopyListView(LoginRequiredMixin, generic.ListView, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '2/m'
    ratelimit_block = True

    model = book_models.Copy


class CopyDetailView(LoginRequiredMixin, generic.DetailView, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    model = book_models.Copy


class CopyReserveView(LoginRequiredMixin, generic.View, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request, pk, *args, **kwargs):
        book = book_models.Copy.objects.get(pk=pk)
        book_models.Reservation(person=request.user, book=book).save()
        return HttpResponse('successfully reserved for you.<br><a href="/">Home</a>')


class CopyLoanView(LoginRequiredMixin, generic.View, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request, pk, *args, **kwargs):
        book = book_models.Copy.objects.get(pk=pk)
        book_models.Loan(person=request.user, book=book).save()
        return HttpResponse('Go and get your book.<br><a href="/">Home</a>')


class LoanListView(LoginRequiredMixin, generic.ListView, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    model = book_models.Loan


class Books_Loned_Between_Two_Times_View(LoginRequiredMixin, generic.FormView, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'book/books_loned_between_two_times.html'
    form_class = book_forms.Books_Loned_Between_Two_Times_Form
    success_url = '/'

    def form_valid(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        books = book_models.Loan.objects.filter(date_due__range=[start_date, end_date])
        # return super().form_valid(form)
        # to do its better to change it to render
        context = {'context': books}
        return render(self.request, 'book/template.html', context=context)


class Students_Who_Do_Not_Loan_Any(LoginRequiredMixin, generic.View, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request):

        result = User.objects.exclude(id__in=book_models.Loan.objects.values('person__id'))
        context = {'students': result}
        return render(request, 'book/students_who_do_not_loan_any.html', context=context)


class Authors_Loaned_By_Student(LoginRequiredMixin, generic.FormView, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name = 'book/authors_loaned_by_student.html'
    success_url = '/'
    form_class = book_forms.Authors_Loaned_By_Student_Form

    def form_valid(self, form):
        username = form.cleaned_data['username']
        user_loans = book_models.Loan.objects.filter(person__username__exact=username)
        result = user_loans.values_list('book__book__authors__name',flat=True)
        context = {'context': result}
        return render(self.request, 'book/template.html', context=context)


class HomePageView( generic.TemplateView, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = book_models.Book.objects.all()
        context['NO'] = book_models.Copy.objects.count()
        return context


class Loan_Near_Due_Date(LoginRequiredMixin,generic.TemplateView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name ='book/loan_near_due_date.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = book_models.Loan.objects.filter(date_due__lt=datetime.now().date()-timedelta(days=constants.LOAN_TIME-constants.NEAR))
        context['context'] = queryset
        return context


class Students_Who_Borrow_Books_In_Special_Publish_Year(LoginRequiredMixin,generic.FormView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name = 'book/students_who_borrow_books_in_special_publish_year.html'
    success_url = '/'
    form_class = book_forms.Students_Who_Borrow_Books_In_Special_Publish_Year_Form

    def form_valid(self, form):
        year = form.cleaned_data['year']
        # book_published_in_year = book_models.Copy.objects.filter(book__publish_year__exact=year)
        # result = book_published_in_year.values_list('borrowers__username',flat=True)
        book_published_in_year = book_models.Loan.objects.filter(book__book__publish_year__exact=year)
        result = book_published_in_year.values_list('person__username',flat=True)
        context = {'context': result}
        return render(self.request, 'book/template.html', context=context)


class List_Of_Best_Students(LoginRequiredMixin,generic.TemplateView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name ='book/list_of_best_students.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = User.objects.all()
        context['context'] = queryset
        return context


class Subject_View(LoginRequiredMixin,generic.View,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self,request,subject):
        key = ''
        if subject == 'poem':
            key='P'
        elif subject == 'story':
            key = 'S'
        elif subject == 'magazine':
            key = 'M'
        elif subject == 'history':
            key = 'H'
        elif subject == 'biography':
            key='B'
        result = book_models.Book.objects.filter(subject__exact=key)
        context = {'context': result}
        return render(self.request,template_name='book/book_subject.html',context=context)