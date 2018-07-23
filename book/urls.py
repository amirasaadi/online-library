from django.urls import path
from book import views

app_name = 'book'

urlpatterns = [

    path('<int:pk>/', views.CopyDetailView.as_view(), name='detail_copy'),

    path('',views.CopyListView.as_view(),name='list_copy'),

    path('reserve/<int:pk>/', views.CopyReserveView.as_view(), name='reserve_copy'),
    path('borrow/<int:pk>/', views.CopyLoanView.as_view(), name='borrow_copy'),

    path('loans_list/',views.LoanListView.as_view(),name='list_loan'),

    path(
        'books_loned_between_two_times/',
        views.Books_Loned_Between_Two_Times_View.as_view(),
        name='books_loned_between_two_times'
    ),

    path(
        'students_who_do_not_loan_any/',
        views.Students_Who_Do_Not_Loan_Any.as_view(),
        name='students_who_do_not_loan_any'
    ),

    path(
        'authors_loaned_by_student/',
        views.Authors_Loaned_By_Student.as_view(),
        name='authors_loaned_by_student'
    ),

    path(
        'loan_near_due_date/',
        views.Loan_Near_Due_Date.as_view(),
        name='loan_near_due_date'
    ),

    path(
        'students_who_borrow_books_in_special_publish_year/',
        views.Students_Who_Borrow_Books_In_Special_Publish_Year.as_view(),
        name='students_who_borrow_books_in_special_publish_year'
    ),

    path('subject/<slug:subject>/',views.Subject_View.as_view(),name='subject_book'),

    # returning book
    path('return/',views.Return_Book.as_view(),name='return_book'),

    #reserves CRUD
    path('reserve/delete/<int:pk>/',views.Delete_Reserve_View.as_view(),name='delete_reserve'),
    path('reserve/',views.Reserve_List_View.as_view(),name='list_reserve'),
    path('reserve/detail/<int:pk>/',views.Reserve_Detail_View.as_view(),name='detail_reserve'),
    #loans CRUD
    path('loan/', views.User_Loan_List_View.as_view(), name='user_loans_list'),
    path('loan/<int:pk>/', views.Loan_Detail_View.as_view(), name='detail_loan'),
    path('loan/extend/<int:pk>/',views.Loan_Extend_View.as_view(),name='loan_extend'),
]
