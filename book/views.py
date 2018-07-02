from django.http import HttpResponse
from django.views import generic
from book import models as book_models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



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