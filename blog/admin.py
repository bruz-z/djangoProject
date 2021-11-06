from django.contrib import admin

# Register your models here.
from blog.models import User, Book, Record

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Record)
