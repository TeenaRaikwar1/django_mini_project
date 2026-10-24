from django.urls import path

from . import views


urlpatterns = [

    # Dashboard
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),


    # Students

    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "students/add/",
        views.student_add,
        name="student_add"
    ),

    path(
        "students/update/<int:id>/",
        views.student_update,
        name="student_update"
    ),

    path(
        "students/delete/<int:id>/",
        views.student_delete,
        name="student_delete"
    ),


    # Books

    path(
        "books/",
        views.book_list,
        name="book_list"
    ),

    path(
        "books/add/",
        views.book_add,
        name="book_add"
    ),

    path(
        "books/update/<int:id>/",
        views.book_update,
        name="book_update"
    ),

    path(
        "books/delete/<int:id>/",
        views.book_delete,
        name="book_delete"
    ),


    # Issue / Return

    path(
        "issue/",
        views.issue_book,
        name="issue_book"
    ),

    path(
        "issues/",
        views.issue_list,
        name="issue_list"
    ),

    path(
        "return/<int:id>/",
        views.return_book,
        name="return_book"
    ),
]