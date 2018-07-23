from django.urls import path
from . import views
from django.contrib.auth.views import password_change,password_change_done


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    # path('update/', views.UserUpdateView.as_view(), name='update_user'),
    path('update/',views.edit_profile_view,name='update_user'),
    path('', views.UserDetailView.as_view(), name='detail_user'),
    path('password/',views.change_password,name='change_password'),
]