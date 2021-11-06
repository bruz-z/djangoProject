from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from blog import views
from dtoken import views as dtoken_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user', views.UserViews.as_view()),
    path('api/login', dtoken_views.tokens),
    path('api/user/', include('blog.urls')),
    path('api/users', views.user_list),
    path('api/book/', include('blog.urls')),
    path('api/book', views.BookViews.as_view()),
    path('api/books', views.book_list),
]

