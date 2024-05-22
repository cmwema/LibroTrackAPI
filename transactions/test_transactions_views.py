from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal
from members.models import Member
from books.models import Book
from .models import Transaction


class TransactionModelTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            first_name='caleb',
            last_name='mwema',
            email='caleb.mwema@example.com',
            debt=Decimal('100.00')
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890',
            published_date=date(2022, 1, 1),
            stock=10,
            genre='Test Genre'
        )

    def test_new_transaction_handling(self):
        transaction = Transaction.objects.create(
            book=self.book,
            member=self.member,
            issue_date=date.today(),
            due_date=date.today(),
            fee=Decimal('10.00'),
            paid=False
        )
        self.assertEqual(transaction.book.stock, 9)
        self.assertEqual(transaction.member.debt, Decimal('110.00'))

    def test_existing_transaction_handling(self):
        existing_transaction = Transaction.objects.create(
            book=self.book,
            member=self.member,
            issue_date=date.today(),
            due_date=date.today(),
            fee=Decimal('10.00'),
            paid=False
        )
        existing_transaction.paid = True
        existing_transaction.save()
        self.assertEqual(existing_transaction.book.stock, 10)
        self.assertEqual(existing_transaction.member.debt, Decimal('100.00'))

    def test_high_debt_validation(self):
        self.member.debt = Decimal('500.00')
        self.member.save()
        with self.assertRaises(ValidationError):
            Transaction.objects.create(
                book=self.book,
                member=self.member,
                issue_date=date.today(),
                due_date=date.today(),
                fee=Decimal('10.00'),
                paid=False
            )
