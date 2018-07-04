from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from book import models as book_models
from book import forms as book_forms

from django.contrib.auth.models import User


class BookListView(LoginRequiredMixin,generic.ListView):
    model = book_models.Book


class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = book_models.Book


class BookCreateView(LoginRequiredMixin,generic.CreateView):
    fields = '__all__'
    model = book_models.Book


class BookDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = book_models.Book
    success_url = reverse_lazy('book:list_book')


class BookUpdateView(LoginRequiredMixin,generic.UpdateView):
    fields = '__all__'
    model = book_models.Book


class BookReserveView(LoginRequiredMixin,generic.View):

    def get(self,request,pk,*args,**kwargs):
        book = book_models.Copy.objects.get(pk=pk)
        book_models.Reservation(person=request.user,book=book).save()
        return HttpResponse('successfully reserved for you')


class BookLoanView(LoginRequiredMixin,generic.View):

    def get(self,request,pk,*args,**kwargs):
        book = book_models.Copy.objects.get(pk=pk)
        book_models.Loan(person=request.user,book=book).save()
        return HttpResponse('Go and get your book.')


class LoanListView(LoginRequiredMixin,generic.ListView):
    model = book_models.Loan


class Books_Loned_Between_Two_Times_View(LoginRequiredMixin,generic.FormView):

    template_name = 'book/books_loned_between_two_times.html'
    form_class = book_forms.Books_Loned_Between_Two_Times_Form
    success_url = '/'

    def form_valid(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        books = book_models.Loan.objects.filter(date_due__range=[start_date,end_date])
        # return super().form_valid(form)
        # to do its better to change it to render
        return HttpResponse(books)


class Students_Who_Do_Not_Loan_Any(LoginRequiredMixin,generic.View):
    def get(self,request):
        loaner = book_models.Loan.objects.all()
        lis =[]
        for item in loaner:
            lis.append(item.person)
        result = lis
        result = User.objects.exclude(username__in=lis)
        context ={'students':result}
        # return HttpResponse(result)
        return render(request,'book/students_who_do_not_loan_any.html',context=context)


class Authors_Loaned_By_Student(LoginRequiredMixin,generic.FormView):
    template_name = 'book/authors_loaned_by_student.html'
    success_url = '/'
    form_class = book_forms.Authors_Loaned_By_Student_Form

    def form_valid(self, form):
        username = form.cleaned_data['username']
        # result = book_models.Loan.objects.filter(person__a__borrowers=)
        return HttpResponse('r')

