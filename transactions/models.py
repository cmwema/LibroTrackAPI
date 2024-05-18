from django.core.exceptions import ValidationError
from django.db import models
from decimal import Decimal
from members.models import Member
from books.models import Book
import uuid


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, blank=False, unique=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        print(self.paid)
        if not self.paid:
            self._handle_new_transaction()
        else:
            self._handle_existing_transaction()

        super(Transaction, self).save(*args, **kwargs)

    def _handle_new_transaction(self):
        self.book.stock -= 1
        self.book.save()

        if self.member.debt + self.fee >= Decimal('500.00'):
            raise ValidationError('Member has debt of 500 or more and cannot borrow a book.')
        self.member.debt += self.fee
        self.member.save()

    def _handle_existing_transaction(self):
        if self.paid and not Transaction.objects.get(pk=self.pk).paid:
            self.book.stock += 1
            self.book.save()

            if not self.member.debt - self.fee < Decimal('0'):
                self.member.debt -= self.fee
                self.member.save()
