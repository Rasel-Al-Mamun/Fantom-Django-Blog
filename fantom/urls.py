from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from django.conf.urls.static import static
from django.urls import path, include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^admin/filebrowser/', site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
    
    path('', include('home.urls', namespace='home')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('user/', include('user.urls', namespace='user')),
    path('auth/', include('authentication.urls', namespace='auth')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
