from django.db import models
import uuid
from decimal import Decimal


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    debt = models.DecimalField(decimal_places=2, max_digits=6, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
