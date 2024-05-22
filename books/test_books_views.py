from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Book
from .serializers import BookSerializer
from datetime import date
import uuid


class BookViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.book1 = Book.objects.create(
            title='Book One',
            author='Author One',
            isbn='1234567890123',
            published_date=date(2020, 1, 1),
            stock=10,
            genre='Fiction'
        )
        self.book2 = Book.objects.create(
            title='Book Two',
            author='Author Two',
            isbn='9876543210987',
            published_date=date(2021, 2, 2),
            stock=5,
            genre='Non-Fiction'
        )

    def test_get_books_list(self):
        response = self.client.get(reverse('book-list'))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        data = {
            'title': 'Book Three',
            'author': 'Author Three',
            'isbn': '1234567890124',
            'published_date': '2022-03-03',
            'stock': 7,
            'genre': 'Science'
        }
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'Book Three')

    def test_get_book_detail(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book1.pk}))
        serializer = BookSerializer(self.book1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_book(self):
        data = {
            'title': 'Updated Book One',
            'author': 'Author One',
            'isbn': '1234567890123',
            'published_date': '2020-01-01',
            'stock': 12,
            'genre': 'Fiction'
        }
        response = self.client.put(reverse('book-detail', kwargs={'pk': self.book1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')
        self.assertEqual(self.book1.stock, 12)

    def test_delete_book(self):
        response = self.client.delete(reverse('book-detail', kwargs={'pk': self.book1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
