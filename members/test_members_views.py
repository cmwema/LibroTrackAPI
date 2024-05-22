from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Member
from .serializers import MemberSerializer


class MemberViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.member1 = Member.objects.create(first_name='caleb', last_name='mwema', email='caleb.mwema@example.com',
                                             debt=Decimal('10.50'))
        self.member2 = Member.objects.create(first_name='mwema', last_name='mwema', email='mwema.mwema@example.com',
                                             debt=Decimal('20.75'))

    def test_get_members_list(self):
        response = self.client.get(reverse('member-list'))
        members = Member.objects.all()
        # print(members)
        serializer = MemberSerializer(members, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_member(self):
        data = {
            'first_name': 'caleb',
            'last_name': 'Johnson',
            'email': 'caleb.johnson@example.com',
            'debt': '0.00'
        }
        # print(reverse('member-list'))
        response = self.client.post(reverse('member-list'), data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 3)
        self.assertEqual(Member.objects.get(id=response.data['id']).first_name, 'caleb')

    def test_get_member_detail(self):
        # print(reverse('member-detail', kwargs={'pk': self.member1.pk}))
        response = self.client.get(reverse('member-detail', kwargs={'pk': self.member1.pk}))
        serializer = MemberSerializer(self.member1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_member(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@newexample.com',
            'debt': '15.00'
        }
        response = self.client.put(reverse('member-detail', kwargs={'pk': self.member1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.member1.refresh_from_db()
        self.assertEqual(self.member1.email, 'john.doe@newexample.com')
        self.assertEqual(self.member1.debt, Decimal('15.00'))

    def test_delete_member(self):
        response = self.client.delete(reverse('member-detail', kwargs={'pk': self.member1.pk}))
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Member.objects.count(), 1)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('member-list'))
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
