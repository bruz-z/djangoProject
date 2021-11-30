from django.contrib import admin

# Register your models here.
from blog.models import User, Book, Record


class UserAdmin(admin.ModelAdmin):
    list_display = ('Id', 'Username', 'Password', 'Email', 'Nickname')
    list_filter = ('Username', 'Nickname')
    list_per_page = 10


class BookAdmin(admin.ModelAdmin):
    list_display = ('Id', 'Name', 'Place', 'Introduction', 'Author', 'Price')
    list_filter = ('Author', 'Price')
    list_per_page = 10


class RecordAdmin(admin.ModelAdmin):
    list_display = ('Id', 'BookId', 'UserId', 'BorrowDate', 'ReturnDate')
    list_filter = ('BorrowDate', 'ReturnDate')
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Record, RecordAdmin)
