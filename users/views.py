from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from users import models as user_models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/users_detail.html'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = '__all__'
    model = user_models.User
