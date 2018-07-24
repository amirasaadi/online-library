from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from book import models as book_models
from book import forms as book_forms

from django.contrib.auth.models import User

# ip blocking
from ratelimit.mixins import RatelimitMixin


# for number of books and avibility in homepage
from django.db.models import Count

from datetime import date
from datetime import timedelta

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
        book.LOAN_STATUS = 'r'
        return HttpResponse('successfully reserved for you.<br><a href="/">Home</a>')


class CopyLoanView(LoginRequiredMixin, generic.View, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request, pk, *args, **kwargs):
        book = book_models.Copy.objects.get(pk=pk)
        user = request.user
        reservers = book_models.Reservation.objects.filter(book=book).order_by('-date_reserved')[0]
        if reservers:
            if reservers.person == user:
                # creating loan object
                book_models.Loan(person=request.user, book=book).save()
                #delete object
                reservers.delete()
                return HttpResponse('Go and get your book.<br><a href="/">Home</a>')


            else:
                return HttpResponse('Sorry this book is reserved. try another time.<br><a href="/">Home</a>')
        else:
            book_models.Loan(person=request.user, book=book).save()
        book.LOAN_STATUS = 'o'




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
        context = book_models.Book.books_loned_between_two_times(start_date,end_date)
        return render(self.request, 'book/template.html', context=context)


class Students_Who_Do_Not_Loan_Any(LoginRequiredMixin, generic.View, RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request):
        context = book_models.Book.students_who_do_not_loan_any()
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
        context = book_models.Book.authors_loaned_by_student(username)
        return render(self.request, 'book/template.html', context=context)


class HomePageView( generic.TemplateView, RatelimitMixin):

    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = book_models.Book.objects.annotate(num_books=Count('copy'))
        context ['books'] = books
        return context


class Loan_Near_Due_Date(LoginRequiredMixin,generic.TemplateView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name ='book/loan_near_due_date.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = book_models.Book.loan_near_due_date()
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
        context = book_models.Book.students_who_borrow_books_in_special_publish_year(year)
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


class Return_Book(LoginRequiredMixin,generic.FormView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name = 'book/return_book.html'
    form_class = book_forms.Return_Book_Form

    def form_valid(self, form):
        username = form.cleaned_data['username']
        book_id = form.cleaned_data['copy_id']

        loan = book_models.Loan.objects.get(book__book_id=book_id , person__username__exact=username)
        if loan:
            loan.due_back=date.today()
            loan.book.LOAN_STATUS = 'a'
            context = 'operation succsefully done!'
        else:
            context = 'loan not found!  '
        return render(self.request, 'book/template.html', context)


class Delete_Reserve_View(LoginRequiredMixin,generic.View,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self,request,pk):
        reserve = book_models.Reservation.objects.get(pk=pk)
        if reserve.person== self.request.user:
            reserve.delete()
        return HttpResponseRedirect(reverse_lazy('book:list_reserve'))


class Reserve_List_View(LoginRequiredMixin,generic.TemplateView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name ='book/reserve_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        reserve_list = book_models.Reservation.objects.filter(person=user)
        context['rserve_list'] = reserve_list
        return context


class Reserve_Detail_View(LoginRequiredMixin,generic.TemplateView,RatelimitMixin):

    def get(self, request,pk):
        reserved = book_models.Reservation.objects.get(pk=pk)
        return render(request, 'book/reservestatus_detail.html', context={'reservestatus':reserved})


class User_Loan_List_View(LoginRequiredMixin,generic.TemplateView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'book/user_loan_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        loan_list = book_models.Loan.objects.filter(person=user)
        context['loan_list'] = loan_list
        return context


class Loan_Detail_View(LoginRequiredMixin,generic.TemplateView,RatelimitMixin):
    def get(self, request,pk):
        loaned = book_models.Loan.objects.get(pk=pk)
        return render(
            request,
            'book/loanstatus_detail.html',
            context={'loanstatus':loaned,'due':loaned.date_due+timedelta(days=constants.LOAN_TIME)}
        )


class Loan_Extend_View(LoginRequiredMixin,generic.View,RatelimitMixin):
    def get(self,request,pk):
        loan = book_models.Loan.objects.get(pk=pk)
        if loan.person== self.request.user:

            temp_loan = book_models.Loan()
            temp_loan.person = loan.person
            temp_loan.book = loan.book

            if temp_loan.can_loan():
                temp_loan.extend_loan(pk)

            # is this neccessary
            # temp_loan.delete()

        return HttpResponseRedirect(reverse_lazy('book:user_loans_list'))
