from django import forms
from book.models import Loan


class Books_Loned_Between_Two_Times_Form(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()


class Authors_Loaned_By_Student_Form(forms.Form):
    username = forms.CharField(max_length=255)