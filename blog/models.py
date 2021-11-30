from django.db import models


class User(models.Model):
    Id = models.AutoField(primary_key=True, verbose_name='用户id')
    Username = models.CharField(max_length=15, verbose_name='用户名')
    Password = models.CharField(max_length=30, verbose_name='密码')
    Email = models.EmailField()
    Nickname = models.CharField(max_length=15, verbose_name='昵称')

    def __str__(self):
        return '{},{},{},{},{}'.format(self.Id, self.Username, self.Password, self.Email, self.Nickname)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Book(models.Model):
    Id = models.AutoField(primary_key=True, verbose_name='书id')
    Name = models.CharField(max_length=30, verbose_name='书名')
    Place = models.CharField(max_length=30, verbose_name='位置')
    Introduction = models.CharField(max_length=30, verbose_name='简介')
    Author = models.CharField(max_length=30, verbose_name='作者')
    Price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='价格')

    def __str__(self):
        return '{},{},{},{},{},{}'.format(self.Id, self.Name, self.Place, self.Introduction, self.Author, self.Price)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Record(models.Model):
    Id = models.AutoField(primary_key=True, verbose_name='记录id')
    BookId = models.IntegerField(verbose_name='书id')
    UserId = models.IntegerField(verbose_name='用户id')
    BorrowDate = models.DateTimeField(auto_now_add=True)
    ReturnDate = models.DateTimeField(null=True)
    BookId = models.ForeignKey('Book', on_delete=models.CASCADE)
    UserId = models.ForeignKey('User', on_delete=models.CASCADE)

    def to_dict(self):
        # 重写model_to_dict()方法转字典
        from datetime import datetime

        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(f, models.FileField):
                value = value.url if value else None
            data[f.name] = value
        return data

    def __str__(self):
        return '{},{},{},{},{}'.format(self.Id, self.BookId, self.UserId, self.BorrowDate, self.ReturnDate)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"
