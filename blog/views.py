import json
import datetime
from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from .models import *
from django.http import JsonResponse
from django.views import View
from tools.logging_check import logging_check
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# @logging_check
def user_list(request):  # api/users
    if request.method != 'GET':
        result = {'code': 0, 'msg': 'use GET！'}
        return JsonResponse(result)
    users = User.objects.all()
    tmp = []
    for user in users:
        user = model_to_dict(user)
        del user['Password'], user['Email'], user['Nickname']
        tmp.append(user)
    result = {'code': 0, 'msg': 'acquire user list successfully!', 'data': tmp}
    return JsonResponse(result)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def change_password(request):  # api/user/password
    json_str = request.body
    json_obj = json.loads(json_str)
    user_id = json_obj.get('user_id')
    password_new = json_obj.get('password')
    password_old = json_obj.get('old_password')
    #user = request.myuser
    try:
        user = User.objects.get(Id=user_id)
    except Exception:
        result = {'code': 0, 'msg': 'user_id is not exist!'}
        return JsonResponse(result)
    if password_old != user.Password:
        result = {'code': 0, 'msg': '原始密码错误!'}
        return JsonResponse(result)
    else:
        user.Password = password_new
        user.save()
        result = {'code': 1, 'msg': '密码修改成功！'}
        return JsonResponse(result)


class UserViews(View):  # api/user
    def get(self, request, username=None):
        user_id = request.GET.get('user_id')
        try:
            user = User.objects.get(Id=user_id)
        except Exception:
            result = {'code': 0, 'msg': 'user not exist'}
            return JsonResponse(result)
        result = {'code': 1, 'msg': 'acquire user information successfully!',
                  'data': {'username': user.Username, 'nickname': user.Nickname, 'email': user.Email}}
        return JsonResponse(result)

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj.get('username')
        password = json_obj.get('password')
        email = json_obj.get('email')
        nickname = json_obj.get('nickname')
        old_user = User.objects.filter(Username=username)
        if old_user:
            result = {'code': 0, 'msg': 'username already exist!'}
            return JsonResponse(result)
        old_email = User.objects.filter(Email=email)
        if old_email:
            result = {'code': 0, 'msg': 'email already registered!'}
            return JsonResponse(result)
        # 创建用户
        count = User.objects.count()
        try:
            User.objects.create(Id=count + 1, Username=username, Password=password,
                                Nickname=nickname, Email=email)
        except Exception as e:
            print(e)
            result = {'code': 0, 'msg': 'msg!'}
            return JsonResponse(result)
        result = {'code': 1, 'msg': 'create success!', 'data': count + 1}
        return JsonResponse(result)

    #@method_decorator(logging_check)
    def put(self, request, username=None):
        json_str = request.body
        json_obj = json.loads(json_str)
        # user = request.myuser
        user_id = json_obj.get('user_id')
        email = json_obj.get('email')
        nickname = json_obj.get('nickname')
        try:
            user = User.objects.get(Id=user_id)
        except Exception:
            result = {'code': 0, 'msg': 'user_id is not exist!'}
            return JsonResponse(result)
        old_email = list(User.objects.values_list('Email'))
        for i in old_email:
            if email == i[0]:
                result = {'code': 0, 'msg': 'the email is occupied!'}
                return JsonResponse(result)
        User.objects.filter(Id=user_id).update(Id=user_id, Email=email, Nickname=nickname)
        return JsonResponse({'code': 1, 'msg': 'change success!'})


def borrow_book(request):  # api/book/borrow
    json_str = request.body
    json_obj = json.loads(json_str)
    book_id = json_obj.get('book_id')
    user_id = json_obj.get('user_id')
    try:
        Book.objects.get(Id=book_id)
    except Exception:
        result = {'code': 0, 'msg': 'book_id is not exist!'}
        return JsonResponse(result)
    try:
        User.objects.get(Id=user_id)
    except Exception:
        result = {'code': 0, 'msg': 'user_id is not exist!'}
        return JsonResponse(result)
    count = Record.objects.count()
    try:
        record = Record.objects.get(BookId=book_id, UserId=user_id)
    except:
        Record.objects.create(Id=count + 1, BookId=book_id, UserId=user_id)
        result = {'code': 1, 'msg': 'borrow success!',
                  'data': {'record_id': count + 1, 'borrow_date': datetime.datetime.now()}}
        return JsonResponse(result)
    if record.ReturnDate is None:  # 为啥这里就可以record.
        result = {'code': 0, 'msg': 'the book has been borrowed!'}
        return JsonResponse(result)
    else:
        Record.objects.create(Id=count + 1, BookId=book_id, UserId=user_id)
    result = {'code': 1, 'msg': 'borrow success!',
              'data': {'record_id': count + 1, 'borrow_date': datetime.datetime.now()}}
    return JsonResponse(result)


class BookViews(View):  # api/book
    def get(self, request):
        book_id = request.GET.get('book_id')
        try:
            book = Book.objects.get(Id=book_id)
        except:
            result = {'code': 0, 'msg': 'The book is not exist'}
            return JsonResponse(result)
        result = {'code': 1, 'msg': 'acquire book information successfully!',
                  'data': {'name': book.Name, 'place': book.Place, 'introduction': book.Introduction,
                           'author': book.Author, 'price': book.Price}}
        return JsonResponse(result)

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        name = json_obj.get('name')
        place = json_obj.get('place')
        introduction = json_obj.get('introduction')
        author = json_obj.get('author')
        price = json_obj.get('price')
        count = Book.objects.count()
        Book.objects.create(Id=count + 1, Name=name, Place=place, Introduction=introduction, Author=author, Price=price)
        result = {'code': 1, 'msg': 'create success!', 'data': count + 1}  # 返回 .Id报错
        return JsonResponse(result)

    def put(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        name = json_obj.get('name')
        place = json_obj.get('place')
        introduction = json_obj.get('introduction')
        author = json_obj.get('author')
        price = json_obj.get('price')
        book_id = json_obj.get('book_id')
        try:
            book = Book.objects.get(Id=book_id)
        except:
            return JsonResponse({'code': 0, 'msg': 'The book is not exist!'})
        Book.objects.filter(Id=book_id).update(Name=name, Place=place, Introduction=introduction,
                                               Author=author, Price=price)
        result = {'code': 1, 'msg': 'change success!',
                  'data': {'name': name, 'place': place, 'introduction': introduction,
                           'author': author, 'price': price}}
        return JsonResponse(result)

    def delete(self, request):
        book_id = request.GET.get('book_id')
        try:
            book = Book.objects.get(Id=book_id)
        except:
            result = {'code': 0, 'msg': 'The book is not exist!'}
            return JsonResponse(result)
        name = book.Name
        place = book.Place
        introduction = book.Introduction
        author = book.Author
        price = book.Price
        book.delete()
        result = {'code': 1, 'msg': 'delete success!',
                  'data': {'name': name, 'place': place, 'introduction': introduction,
                           'author': author, 'price': price}}
        return JsonResponse(result)


def check_status(request):  # api/book/status
    if request.method != 'GET':
        result = {'code': 0, 'msg': 'use GET！'}
        return JsonResponse(result)
    book_id = request.GET.get('book_id')
    try:
        record = Record.objects.get(BookId=book_id)
    except:
        result = {'code': 0, 'msg': 'the book is not exist!'}
        return JsonResponse(result)
    result = {'code': 1, 'msg': 'acquire record successfully!',
              'data': {'user_id': record.UserId, 'borrow_date': record.BorrowDate, 'return_date': record.ReturnDate}}
    return JsonResponse(result)


def book_list(request):  # api/books
    if request.method != 'GET':
        result = {'code': 0, 'msg': 'use GET！'}
        return JsonResponse(result)
    books = Book.objects.all()
    tmp = []
    for book in books:
        book = model_to_dict(book)
        del book['Place'], book['Introduction'], book['Author'], book['Price']
        tmp.append(book)
    result = {'code': 0, 'msg': 'acquire book list successfully!', 'data': tmp}
    return JsonResponse(result)


def book_records(request):  # api/book/records
    if request.method != 'GET':
        result = {'code': 0, 'msg': 'use GET！'}
        return JsonResponse(result)
    book_id = request.GET.get('book_id')
    records = Record.objects.filter(BookId=book_id)
    if not records:
        result = {'code': 0, 'msg': 'the book is not exist!'}
        return JsonResponse(result)
    tmp = []  # 获取对应用户名
    for record in records:
        user = User.objects.get(Id=record.UserId)
        tmp.append(user.Username)
    ls = []  # 获取对应借还记录
    i = 0
    for record in records:
        record = record.to_dict()
        del record['BookId']
        record['username'] = tmp[i]
        i += 1
        ls.append(record)
    result = {'code': 1, 'msg': 'acquire records successfully!', 'data': ls}
    return JsonResponse(result)


def user_records(request):  # api/user/books
    if request.method != 'GET':
        result = {'code': 0, 'msg': 'use GET！'}
        return JsonResponse(result)
    user_id = request.GET.get('user_id')
    records = Record.objects.filter(UserId=user_id)
    if not records:
        result = {'code': 0, 'msg': 'the user is not exist!'}
        return JsonResponse(result)
    tmp = []  # 获取对应书名
    for record in records:
        book = Book.objects.get(Id=record.BookId)
        tmp.append(book.Name)
    ls = []  # 获取对应借还记录
    i = 0
    for record in records:
        record = record.to_dict()
        del record['UserId']
        record['name'] = tmp[i]
        i += 1
        ls.append(record)
    result = {'code': 1, 'msg': 'acquire records successfully!', 'data': ls}
    return JsonResponse(result)


def book_return(request):  # api/book/return
    json_str = request.body
    json_obj = json.loads(json_str)
    record_id = json_obj.get('record_id')
    user_id = json_obj.get('user_id')
    try:
        user = User.objects.get(Id=user_id)
    except:
        result = {'code': 0, 'msg': 'the user is not exist!'}
        return JsonResponse(result)
    try:
        record = Record.objects.get(Id=record_id)
    except:
        result = {'code': 0, 'msg': 'the record is not exist!'}
        return JsonResponse(result)
    if user.Id != record.UserId:
        result = {'code': 0, 'msg': 'the user is not correspond to the record!'}
        return JsonResponse(result)
    record.ReturnDate = datetime.datetime.now()
    record.save()
    result = {'code': 1, 'msg': 'return success!',
              'data': {'borrow_date': record.BorrowDate, 'return_date': record.ReturnDate}}
    return JsonResponse(result)


def book_record(request):  # api/book/record
    if request.method != 'GET':
        result = {'code': 0, 'msg': 'use GET！'}
        return JsonResponse(result)
    record_id = request.GET.get('record_id')
    try:
        record = Record.objects.get(Id=record_id)
    except:
        result = {'code': 0, 'msg': 'the record is not exist!'}
        return JsonResponse(result)
    result = {'code': 1, 'msg': 'acquire record successfully!',
              'data': {'book_id': record.BookId, 'user_id': record.UserId,
                       'borrow_date': record.BorrowDate, 'return_date': record.ReturnDate}}
    return JsonResponse(result)
