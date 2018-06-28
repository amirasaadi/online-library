from django.urls import path
from book import views

app_name = 'book'

urlpatterns = [
    path('create/',views.BookCreateView.as_view(),name='create_book'),
    path('<int:pk>/',views.BookDetailView.as_view(),name='detail_book'),
    path('update/<int:pk>/',views.BookUpdateView.as_view(),name='update_book'),
    path('',views.BookListView.as_view(),name='list_book'),
    path('delete/<int:pk>/',views.BookDeleteView.as_view(),name='delete_book'),

    # path('reserve/<int:pk>/',views.BookReserveView.as_view(),name='reserve_book'),
    # path('borrow/<int:pk>/',views.BookBorrowView.as_view(),name='borrow_book'),
]
