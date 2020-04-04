from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('api/', include(('api.urls', 'api'), namespace='api-home')),
    path('admin/', admin.site.urls),
]
