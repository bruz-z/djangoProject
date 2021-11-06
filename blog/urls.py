from django.urls import path
from . import views

urlpatterns = [
    path('password', views.change_password),
    path('borrow', views.borrow_book),
    path('status', views.check_status),
    path('records', views.book_records),
    path('return', views.book_return),
    path('record', views.book_record),
    path('books', views.user_records),
]