from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from .models import Transaction
from .serializers import TransactionSerializer
from decimal import Decimal


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        member = serializer.validated_data['member']
        self._handle_member_debt(member, serializer.validated_data['paid'], serializer.validated_data['fee'])
        serializer.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        member = instance.member

        new_paid_status = serializer.validated_data.get('paid', instance.paid)
        new_fee = serializer.validated_data.get('fee', instance.fee)

        self._update_member_debt(member, instance.paid, new_paid_status, new_fee)
        serializer.save()

    def _update_member_debt(self, member, current_paid_status, new_paid_status, fee):
        if current_paid_status and not new_paid_status:
            member.debt += fee
        elif not current_paid_status and new_paid_status:
            member.debt -= fee

        member.save()

    def _handle_member_debt(self, member, paid, fee):
        if not paid and member.debt >= Decimal('500.00'):
            raise ValidationError('Member has debt of 500 or more and cannot borrow a book.')
        if not paid:
            member.debt += fee
        member.save()
