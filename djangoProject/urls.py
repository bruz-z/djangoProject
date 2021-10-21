
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from blog import views as user_views
from dtoken import views as dtoken_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/users', user_views.UserViews.as_view()),
    path('v1/tokens', dtoken_views.tokens),
    path('v1/users/', include('blog.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
