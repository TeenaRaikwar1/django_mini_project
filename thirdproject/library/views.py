from django.contrib import messages

from django.db import transaction

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.utils import timezone


from .models import Student, Book, Issue

from .forms import (
    StudentForm,
    BookForm,
    IssueForm
)


# =========================
# DASHBOARD
# =========================

def dashboard(request):

    books = Book.objects.all()


    context = {

        "student_count":
            Student.objects.count(),

        "book_count":
            Book.objects.count(),

        "available_books":
            sum(
                book.available_quantity
                for book in books
            ),

        "issued_count":
            Issue.objects.filter(
                status="Issued"
            ).count(),

        "recent_issues":
            Issue.objects.select_related(
                "student",
                "book"
            )[:5]

    }


    return render(
        request,
        "library/dashboard.html",
        context
    )


# =========================
# STUDENT
# =========================

def student_list(request):

    students = Student.objects.all()


    return render(

        request,

        "library/student_list.html",

        {
            "students": students
        }

    )


def student_add(request):

    if request.method == "POST":

        form = StudentForm(
            request.POST
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Student added successfully."
            )


            return redirect(
                "student_list"
            )


    else:

        form = StudentForm()


    return render(

        request,

        "library/student_form.html",

        {
            "form": form,

            "title": "Add Student",

            "button": "Save Student"
        }

    )


def student_update(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )


    if request.method == "POST":

        form = StudentForm(

            request.POST,

            instance=student

        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Student updated successfully."
            )


            return redirect(
                "student_list"
            )


    else:

        form = StudentForm(
            instance=student
        )


    return render(

        request,

        "library/student_form.html",

        {
            "form": form,

            "title": "Update Student",

            "button": "Update Student"
        }

    )


def student_delete(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )


    if request.method == "POST":

        student.delete()


        messages.success(
            request,
            "Student deleted successfully."
        )


    return redirect(
        "student_list"
    )


# =========================
# BOOK
# =========================

def book_list(request):

    books = Book.objects.all()


    return render(

        request,

        "library/book_list.html",

        {
            "books": books
        }

    )


def book_add(request):

    if request.method == "POST":

        form = BookForm(
            request.POST
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Book added successfully."
            )


            return redirect(
                "book_list"
            )


    else:

        form = BookForm()


    return render(

        request,

        "library/book_form.html",

        {
            "form": form,

            "title": "Add Book",

            "button": "Save Book"
        }

    )


def book_update(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )


    if request.method == "POST":

        form = BookForm(

            request.POST,

            instance=book

        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Book updated successfully."
            )


            return redirect(
                "book_list"
            )


    else:

        form = BookForm(
            instance=book
        )


    return render(

        request,

        "library/book_form.html",

        {
            "form": form,

            "title": "Update Book",

            "button": "Update Book"
        }

    )


def book_delete(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )


    if request.method == "POST":

        active_issue = Issue.objects.filter(

            book=book,

            status="Issued"

        ).exists()


        if active_issue:

            messages.error(

                request,

                "This book cannot be deleted "
                "because it is currently issued."
            )

        else:

            book.delete()


            messages.success(

                request,

                "Book deleted successfully."
            )


    return redirect(
        "book_list"
    )


# =========================
# ISSUE BOOK
# =========================

@transaction.atomic
def issue_book(request):

    if request.method == "POST":

        form = IssueForm(
            request.POST
        )


        if form.is_valid():

            issue = form.save(
                commit=False
            )


            book = Book.objects.select_for_update().get(

                pk=issue.book.pk

            )


            if book.available_quantity <= 0:

                form.add_error(

                    "book",

                    "This book is no longer available."
                )

            else:

                book.available_quantity -= 1

                book.save(
                    update_fields=[
                        "available_quantity"
                    ]
                )


                issue.save()


                messages.success(

                    request,

                    f"'{book.title}' issued "
                    f"to {issue.student.name} successfully."
                )


                return redirect(
                    "issue_list"
                )


    else:

        form = IssueForm()


    return render(

        request,

        "library/issue_form.html",

        {
            "form": form
        }

    )


# =========================
# ISSUE LIST
# =========================

def issue_list(request):

    issues = Issue.objects.select_related(

        "student",

        "book"

    )


    return render(

        request,

        "library/issue_list.html",

        {
            "issues": issues
        }

    )


# =========================
# RETURN BOOK
# =========================

@transaction.atomic
def return_book(request, id):

    issue = get_object_or_404(

        Issue.objects.select_related(

            "student",

            "book"

        ),

        id=id

    )


    if request.method == "POST":

        if issue.status == "Returned":

            messages.warning(

                request,

                "This book has already been returned."
            )

        else:

            book = Book.objects.select_for_update().get(

                pk=issue.book.pk

            )


            if book.available_quantity < book.quantity:

                book.available_quantity += 1

                book.save(

                    update_fields=[
                        "available_quantity"
                    ]

                )


            issue.status = "Returned"

            issue.return_date = (
                timezone.localdate()
            )


            issue.save(

                update_fields=[
                    "status",
                    "return_date"
                ]

            )


            messages.success(

                request,

                f"'{book.title}' returned "
                f"successfully by {issue.student.name}."
            )


    return redirect(
        "issue_list"
    )