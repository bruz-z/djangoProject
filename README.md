## Django+Mysql做的图书管理系统
纯后端+数据库，太菜了弄不来前端

Django配置mysql

+ 创建数据库mysql
+ 更改settings.py：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '自己的name',
        'USER': '自己的user',
        'PASSWORD': '自己的password',
        'HOST': '127.0.0.1',
        'POST': '3306'
    }
}
```

还需要装一些包

```python
pip install mysqlclient
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers #解决前后端跨域问题，本项目中用不到
```

可能还需要下别的包，记不得了，反之缺啥补啥呗