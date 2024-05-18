from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login
from books.views import BookViewSet
from members.views import MemberViewSet
from transactions.views import TransactionViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'members', MemberViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/login", login),
    path("api/", include(router.urls))
]
