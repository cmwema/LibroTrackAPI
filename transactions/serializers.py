from rest_framework import serializers
from .models import Transaction
from decimal import Decimal
from members.serializers import MemberSerializer
from books.serializers import BookSerializer


class TransactionSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_member_name(self, obj):
        return f"{obj.member.first_name} {obj.member.last_name}"

    def get_book_title(self, obj):
        return obj.book.title

    def validate(self, data):
        member = data.get('member')
        paid = data.get('paid', False)

        if not paid and member and member.debt >= Decimal('500.00'):
            raise serializers.ValidationError('Member has debt of 500 or more and cannot borrow a book.')

        return data
