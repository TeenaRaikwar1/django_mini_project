from django.db import models
from django.core.validators import MinValueValidator


class Student(models.Model):

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    course = models.CharField(
        max_length=100
    )

    semester = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    address = models.TextField()


    class Meta:

        ordering = [
            "student_id"
        ]


    def __str__(self):

        return f"{self.student_id} - {self.name}"


class Book(models.Model):

    title = models.CharField(
        max_length=200
    )

    author = models.CharField(
        max_length=150
    )

    category = models.CharField(
        max_length=100
    )

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    available_quantity = models.PositiveIntegerField(
        default=1
    )


    class Meta:

        ordering = [
            "title"
        ]


    def __str__(self):

        return f"{self.title} - {self.author}"


class Issue(models.Model):

    STATUS_CHOICES = [

        ("Issued", "Issued"),

        ("Returned", "Returned"),

    ]


    student = models.ForeignKey(

        Student,

        on_delete=models.CASCADE,

        related_name="issues"
    )


    book = models.ForeignKey(

        Book,

        on_delete=models.CASCADE,

        related_name="issues"
    )


    issue_date = models.DateField(

        auto_now_add=True
    )


    due_date = models.DateField()


    return_date = models.DateField(

        null=True,

        blank=True
    )


    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="Issued"
    )


    class Meta:

        ordering = [
            "-issue_date"
        ]


    def __str__(self):

        return (
            f"{self.student.name} - "
            f"{self.book.title} - "
            f"{self.status}"
        )