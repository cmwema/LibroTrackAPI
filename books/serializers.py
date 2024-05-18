from rest_framework import serializers
from .models import Book
# import isbnlib


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # def validate_isbn(self, value):
    #     if not isbnlib.is_isbn10(value) and not isbnlib.is_isbn13(value):
    #         raise serializers.ValidationError(f'{value} is not a valid ISBN-10 or ISBN-13.')
    #     return value

