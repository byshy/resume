from django.conf.urls import url, include
from . import views


pp_resource = views.PPResource()
user_resource = views.UserResource()

urlpatterns = [
    url(r'^v1/pp', include(pp_resource.urls)),
    url(r'^v1/users', include(user_resource.urls)),
]
