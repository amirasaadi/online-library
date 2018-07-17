from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from users.models import Profile
from django import forms



# class Edit_Profile_Form(UserChangeForm):
#
#
#     class Meta:
#         # model = User
#         model = Profile
#         fields = (
#             'user',
#             'image',
#         )


# class Edit_Profile_Form(forms.Form):
#     firsname = forms.CharField()
#     lastname = forms.CharField()
#     image = forms.ImageField()
#     password1 = forms.PasswordInput()
#     password2 = forms.PasswordInput()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'image',
        )