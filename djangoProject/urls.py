from django.contrib import admin
from django.urls import path, include
from blog import views
from rest_framework_simplejwt.views import TokenRefreshView
from blog.views import MyObtainTokenPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user', views.UserViews.as_view()),
    path('api/register', views.register),
    path('api/user/', include('blog.urls')),
    path('api/users', views.user_list),
    path('api/book/', include('blog.urls')),
    path('api/book', views.BookViews.as_view()),
    path('api/books', views.book_list),
]

