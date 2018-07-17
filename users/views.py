from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from users import models as user_models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from users.forms import ProfileEditForm,UserEditForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render


# ip blocking
from ratelimit.mixins import RatelimitMixin

class SignUp(generic.CreateView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserDetailView(LoginRequiredMixin, generic.TemplateView,RatelimitMixin):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'users/users_detail.html'


# class UserUpdateView(LoginRequiredMixin, generic.UpdateView,RatelimitMixin):
#     ratelimit_key = 'ip'
#     ratelimit_rate = '100/m'
#     ratelimit_block = True
#     fields = '__all__'
#     model = user_models.User
#     # fields = ('','')


# def edit_profile(request):
#     if request.method == 'POST':
#         form = Edit_Profile_Form(request.POST,instance=request.user)
#
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#
#     else:
#         form=Edit_Profile_Form(instance=request.user)
#         args = {'form':form}
#         return render(request,'users/users_form.html',args)


# def edit_profile_view(request):
#     form = Edit_Profile_Form()
#     return render(request,'users/users_form.html',{'form':form})


@login_required()
def edit_profile_view(request):
    if request.method=='POST':
        user_form = UserEditForm(data=request.POST or None,instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request,'users/users_form.html',context)



from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:detail_user')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('users:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })