from django import forms

from django.core.exceptions import ValidationError

from .models import Student, Book, Issue


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            "student_id",
            "name",
            "email",
            "phone",
            "course",
            "semester",
            "address",
        ]

        widgets = {

            "address": forms.Textarea(
                attrs={
                    "rows": 3
                }
            )

        }


class BookForm(forms.ModelForm):

    class Meta:

        model = Book

        fields = [
            "title",
            "author",
            "category",
            "isbn",
            "quantity",
        ]


    def clean_quantity(self):

        quantity = self.cleaned_data["quantity"]

        if quantity < 1:

            raise ValidationError(
                "Quantity must be at least 1."
            )

        return quantity


    def save(self, commit=True):

        book = super().save(
            commit=False
        )


        if book.pk:

            old_book = Book.objects.get(
                pk=book.pk
            )

            issued = (
                old_book.quantity
                -
                old_book.available_quantity
            )


            if book.quantity < issued:

                raise ValidationError(
                    f"Quantity cannot be less than "
                    f"issued copies ({issued})."
                )


            book.available_quantity = (
                book.quantity - issued
            )

        else:

            book.available_quantity = book.quantity


        if commit:

            book.save()


        return book


class IssueForm(forms.ModelForm):

    class Meta:

        model = Issue

        fields = [
            "student",
            "book",
            "due_date",
        ]

        widgets = {

            "due_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            )

        }


    def clean_book(self):

        book = self.cleaned_data["book"]


        if book.available_quantity <= 0:

            raise ValidationError(
                "This book is currently unavailable."
            )


        return book