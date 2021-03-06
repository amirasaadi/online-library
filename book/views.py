from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from book import models as book_models
from book import forms as book_forms

from django.contrib.auth.models import User

# ip blocking
from ratelimit.mixins import RatelimitMixin


# for number of books and avibility in homepage
from django.db.models import Count

from datetime import date
from datetime import timedelta

from book import constants

# excel libraries
from openpyxl import Workbook

from django.shortcuts import redirect

# paginator
from django.core.paginator import Paginator

#penalty
from users.models import Profile

#translations
from django.utils.translation import gettext as _

#payment
from zeep import Client


class CopyListView(LoginRequiredMixin ,RatelimitMixin, generic.ListView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    model = book_models.Copy


class CopyDetailView(LoginRequiredMixin,RatelimitMixin ,generic.DetailView ):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    model = book_models.Copy


class CopyReserveView(LoginRequiredMixin,  RatelimitMixin,generic.View):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request, pk, *args, **kwargs):
        book = book_models.Copy.objects.get(pk=pk)
        book_models.Reservation(person=request.user, book=book).save()
        book.LOAN_STATUS = 'r'
        message = _('not successfully reserved for you .')
        return render(request,'book/template.html',{'header':message})


class CopyLoanView(LoginRequiredMixin, RatelimitMixin, generic.View):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request, pk, *args, **kwargs):
        book = book_models.Copy.objects.get(pk=pk)
        user = request.user
        reservers = book_models.Reservation.objects.filter(book=book).order_by('-date_reserved')[0]
        if reservers:
            if reservers.person == user:
                # creating loan object
                book_models.Loan(person=request.user, book=book).save()
                #delete object
                reservers.delete()
                message = _('Go and get your book.')
                return render(request, 'book/template.html', {'header': message})

            else:
                message = _('Sorry this book is reserved. try another time.')
                return render(request, 'book/template.html', {'header': message})
        else:
            book_models.Loan(person=request.user, book=book).save()
        book.LOAN_STATUS = 'o'




class LoanListView(LoginRequiredMixin,  RatelimitMixin,generic.ListView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    model = book_models.Loan


class Books_Loned_Between_Two_Times_View(LoginRequiredMixin, RatelimitMixin, generic.FormView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'book/books_loned_between_two_times.html'
    form_class = book_forms.Books_Loned_Between_Two_Times_Form
    success_url = '/'

    def form_valid(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        context = book_models.Book.books_loned_between_two_times(start_date,end_date)
        return render(self.request, 'book/template.html', context=context)


class Students_Who_Do_Not_Loan_Any(LoginRequiredMixin, RatelimitMixin, generic.View):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request):
        context = book_models.Book.students_who_do_not_loan_any()
        return render(request, 'book/students_who_do_not_loan_any.html', context=context)


class Authors_Loaned_By_Student(LoginRequiredMixin,RatelimitMixin, generic.FormView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name = 'book/authors_loaned_by_student.html'
    success_url = '/'
    form_class = book_forms.Authors_Loaned_By_Student_Form

    def form_valid(self, form):
        username = form.cleaned_data['username']
        context = book_models.Book.authors_loaned_by_student(username)
        return render(self.request, 'book/template.html', context=context)


class HomePageView( RatelimitMixin ,generic.TemplateView):

    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = book_models.Book.objects.annotate(num_books=Count('copy'))
        paginator = Paginator(books,10)

        page = self.request.GET.get('page')

        # context ['books'] = books
        context['books'] = paginator.get_page(page)
        return context


class Loan_Near_Due_Date(LoginRequiredMixin,RatelimitMixin,generic.TemplateView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name ='book/loan_near_due_date.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = book_models.Book.loan_near_due_date()
        return context


class Students_Who_Borrow_Books_In_Special_Publish_Year(LoginRequiredMixin,RatelimitMixin,generic.FormView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name = 'book/students_who_borrow_books_in_special_publish_year.html'
    success_url = '/'
    form_class = book_forms.Students_Who_Borrow_Books_In_Special_Publish_Year_Form

    def form_valid(self, form):
        year = form.cleaned_data['year']
        context = book_models.Book.students_who_borrow_books_in_special_publish_year(year)
        return render(self.request, 'book/template.html', context=context)


class List_Of_Best_Students(LoginRequiredMixin,RatelimitMixin,generic.TemplateView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name ='book/list_of_best_students.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = User.objects.all()
        context['context'] = queryset
        return context


class Subject_View(LoginRequiredMixin,RatelimitMixin,generic.View):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self,request,subject):
        key = ''
        if subject == 'poem':
            key='P'
        elif subject == 'story':
            key = 'S'
        elif subject == 'magazine':
            key = 'M'
        elif subject == 'history':
            key = 'H'
        elif subject == 'biography':
            key='B'

        result = book_models.Book.objects.filter(subject__exact=key)
        paginator = Paginator(result, 10)
        page = request.GET.get('page')
        # context = {'context': result}
        context = paginator.get_page(page)
        return render(self.request,template_name='book/book_subject.html',context={'context':context})


class Return_Book(LoginRequiredMixin,RatelimitMixin,generic.FormView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    template_name = 'book/return_book.html'
    form_class = book_forms.Return_Book_Form

    def form_valid(self, form):
        book_id = form.cleaned_data['copy_id']

        loan = book_models.Loan.objects.filter(book__book__copy__id=book_id)

        if loan:
            loan[0].due_back=date.today()
            loan[0].book.LOAN_STATUS = 'a'
            loan[0].save()
            delta = loan[0].due_back - loan[0].date_due
            if delta>constants.LOAN_TIME:
                penalty = delta - constants.LOAN_TIME
            else:
                penalty = 0
            last_penalty = Profile.objects.get(user=loan[0].person).penalty
            penalty += last_penalty
            Profile.objects.filter(user=loan[0].person).update(penalty=penalty)
            context = _('operation succsefully done!')
        else:
            context = _('loan not found!')
        return render(self.request, 'book/template.html', {'header':context})


class Delete_Reserve_View(LoginRequiredMixin,RatelimitMixin,generic.View):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self,request,pk):
        reserve = book_models.Reservation.objects.get(pk=pk)
        if reserve.person== self.request.user:
            reserve.delete()
        return HttpResponseRedirect(reverse_lazy('book:list_reserve'))


class Reserve_List_View(LoginRequiredMixin,RatelimitMixin,generic.TemplateView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name ='book/reserve_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        reserve_list = book_models.Reservation.objects.filter(person=user)
        context['rserve_list'] = reserve_list
        return context


class Reserve_Detail_View(LoginRequiredMixin,RatelimitMixin,generic.TemplateView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True

    def get(self, request,pk):
        reserved = book_models.Reservation.objects.get(pk=pk)
        return render(request, 'book/reservestatus_detail.html', context={'reservestatus':reserved})


class User_Loan_List_View(LoginRequiredMixin,RatelimitMixin,generic.TemplateView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    template_name = 'book/user_loan_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        loan_list = book_models.Loan.objects.filter(person=user,due_back__isnull=True)
        context['loan_list'] = loan_list
        return context


class Loan_Detail_View(LoginRequiredMixin,RatelimitMixin,generic.TemplateView):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    def get(self, request,pk):
        loaned = book_models.Loan.objects.get(pk=pk)
        return render(
            request,
            'book/loanstatus_detail.html',
            context={'loanstatus':loaned,'due':loaned.date_due+timedelta(days=constants.LOAN_TIME)}
        )


class Loan_Extend_View(LoginRequiredMixin,RatelimitMixin,generic.View):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    def get(self,request,pk):
        loan = book_models.Loan.objects.get(pk=pk)
        if loan.person== self.request.user:

            temp_loan = book_models.Loan()
            temp_loan.person = loan.person
            temp_loan.book = loan.book

            if temp_loan.can_loan():
                temp_loan.extend_loan(pk)

            # is this neccessary
            # temp_loan.delete()

        return HttpResponseRedirect(reverse_lazy('book:user_loans_list'))


class Export_Excel_View(LoginRequiredMixin,RatelimitMixin,generic.View):
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    def get(self,request):
        wb = Workbook()

        book_sheet = wb.active
        book_sheet.title = 'book'
        # copy_sheet = wb.active
        # copy_sheet.title = 'copy'
        #
        # copy_sheet['A1'] = 'name'
        # copy_sheet['B1'] = 'borrowers'
        # copy_sheet['C1'] = 'reservers'
        # copy_sheet['D1'] = 'loan status'
        #
        # copy_list = book_models.Copy.objects.all()
        # for copy in copy_list:
        #     copy_sheet.append(
        #         [
        #             copy.book.name,
        #             copy.book.id,
        #             copy.book.subject,
        #             copy.get_status_display(),
        #         ]
        #     )


        book_sheet['A1'] = _('name')
        book_sheet['B1'] = _('publish year')
        book_sheet['C1'] = _('ISBN')
        book_sheet['D1'] = _('subject')
        book_sheet['E1'] = _('translators')
        book_sheet['F1'] = _('authors')
        book_sheet['G1'] = _('publishers')
        book_sheet['H1'] = _('count')

        # book_list = book_models.Book.objects.all()
        book_list = book_models.Book.objects.annotate(num_books=Count('copy'))
        for book in book_list:
            book_sheet.append(
                [
                    book.name,
                    book.publish_year,
                    book.ISBN,
                    book.get_subject_display(),
                    ', '.join(translator.name for translator in book.translators.all()),
                    ', '.join(author.name for author in book.authors.all()),
                    book.publishers.name,
                    book.num_books,
                ]
            )

        wb.save('export.xlsx')
        return redirect('/')


#payments

#I request for merchant
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "payment for reserving your book"  # Required
email = 'book@book.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/book/verify/' # Important: need to edit for realy server.

def send_request(request):
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
