from django.db import models
from django.core.exceptions import ValidationError
import uuid
import isbnlib


def validate_isbn(value):
    if not isbnlib.is_isbn13(value) or not isbnlib.is_isbn10(value):
        raise ValidationError(f"{value} is not a valid ISBN-10 or ISBN-13")


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=False)
    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField()
    stock = models.PositiveIntegerField()
    genre = models.CharField(max_length=200)

    def __str__(self):
        return self.title
