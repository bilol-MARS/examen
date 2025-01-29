from django.contrib import admin
from django.urls import path
from apps.views import UserCreateView, UserSigninView, UserLogoutView, IndexView
from root import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserSigninView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
