from rest_framework import generics
from book import models
from book.api import serilezers


class BookListAPIView(generics.ListAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serilezers.BookListSerializer


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serilezers.BookDetailSerialzer
    lookup_field = 'pk'


class BookDeleteAPIView(generics.DestroyAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serilezers.BookDeleteSerialzer
    lookup_field = 'pk'


class BookUpdateAPIView(generics.UpdateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serilezers.BookUpdateSerialzer
    lookup_field = 'pk'


class BookCreateAPIView(generics.CreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serilezers.BookCreateSerialzer


class BookManageAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serilezers.BookManageSerialzer
    lookup_field = 'pk'
