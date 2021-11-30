from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('Id', 'Username')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('Id', 'Name')


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('UserId', 'BorrowDate', 'ReturnDate')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # 添加额外信息
        token['code'] = 200
        token['msg'] = '登录成功!'
        return token
