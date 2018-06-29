from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),

    # path('<int:pk>/', views.UserDetailView.as_view(), name='detail_user'),
    # path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update_user'),

    path('', views.UserDetailView.as_view(), name='detail_user'),

]