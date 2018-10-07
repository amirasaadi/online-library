from django.test import TestCase,Client
import datetime
from django.utils import timezone
from . import models
from django.contrib.auth.models import User

class Book_method_tests(TestCase):

    def test_students_who_do_not_loan_any_with_out_loan(self):
        """this method create temp user then check if it exist in the query"""
        temp_user = User()
        temp_book = models.Book()
        student_list = temp_book.students_who_do_not_loan_any()
        is_temp_user_in_the_list = False
        if temp_user not in list(student_list.values()):
            is_temp_user_in_the_list = True
        self.assertTrue(is_temp_user_in_the_list)

    def test_books_loned_between_two_times_in_future(self):
        start_date = timezone.now() + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=2)
        list_book = models.Book.books_loned_between_two_times(start_date,end_date)
        is_smt_in_list = False
        if list_book['context']:
            is_smt_in_list = True
        self.assertFalse(is_smt_in_list)

    def test_authors_loaned_by_student(self):
        """we create temp user then gime him temp book then check if query is true"""
        temp_user = User.objects.create()
        temp_author = models.Author()
        temp_book = models.Book()
        # temp_book.authors.create(temp_author.id)
        # temp_book.set(temp_author)

        temp_copy = models.Copy(book=temp_book)
        temp_loan = models.Loan(person=temp_user,book=temp_copy)

        aurthors_list = models.Book.authors_loaned_by_student(temp_user.username)
        # print(aurthors_list)
        # print(type(aurthors_list))
        # self.assertQuerysetEqual(aurthors_list,temp_author)

    def test_loan_near_due_date(self):
        pass

    def test_students_who_borrow_books_in_special_publish_year(self):
        pass


class Loan_method_tests(TestCase):

    def test_can_loan(self):
        """we will create temp user and temp book then check if it can loan or not"""
        temp_user = User.objects.create()
        temp_book = models.Book()
        temp_copy = models.Copy(book=temp_book)
        temp_loan = models.Loan(book=temp_copy,person=temp_user)
        can_loan = False
        if temp_loan.can_loan():
            can_loan = True
        self.assertTrue(can_loan)

    def test_extend_loan(self):
        pass

    def test_loan_book_which_dones_not_exist(self):
        """we will create a user and a book but not copy and try to loan it"""
        temp_user = User.objects.create()
        temp_book = models.Book()
        with self.assertRaises(ValueError):
            temp_loan = models.Loan(book=temp_book, person=temp_user)


class Admin_methods_tests(TestCase):

    """ Test case for reserve changing 'status' to 'loan' or 'return back' """

    def test_status_hide(self):
        """
        Test changing all Category instances to 'Hide'
        """
        # Set Queryset to be hidden
        # to_be_hidden = models.Category.objects.values_list('pk', flat=True)
        # Set POST data to be passed to changelist url
        # data = {
        #     'action': 'change_to_hide',
        #     '_selected_action': to_be_hidden
        #     }
        # Set change_url
        # change_url = self.reverse('admin:product_category_changelist')
        # POST data to change_url
        # response = self.post(change_url, data, follow=True)
        # self.assertEqual(
        #     models.Category.objects.filter(status='show').count(), 0
        #     )
