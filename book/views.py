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


class BookReserveView(LoginRequiredMixin,generic.DetailView):

    model = book_models.Reservation
    # def get(self, request,pk):
    #     # <view logic>
    #     book = book_models.Copy.objects.get(pk=pk)
    #     reserve_obj = book_models.Reservation(book=book, person=self.request.user)
    #     reserve_obj.save()
    #     return HttpResponse('you are : '+str(reserve_obj))

# class BookBorrowView(LoginRequiredMixin,generic.ListView):
#     pass

def BookReserveView(request,pk):
    book = book_models.Copy.objects.get(pk=pk)
    reserve_obj = book_models.Reservation(book=book, person=request.user)
    reserve_obj.save()
    return HttpResponse('you are : '+str(reserve_obj))