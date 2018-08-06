from django.urls import path
from book.api import views

app_name = 'api'

urlpatterns = [
    path('list/',views.BookListAPIView.as_view()),
    path('<int:pk>/', views.BookDetailAPIView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.BookDeleteAPIView.as_view(), name='delete'),
    path('update/<int:pk>/', views.BookUpdateAPIView.as_view(), name='update'),
    path('create/', views.BookCreateAPIView.as_view(), name='create'),
    path('manage/<int:pk>/', views.BookManageAPIView.as_view(), name='update'),
]