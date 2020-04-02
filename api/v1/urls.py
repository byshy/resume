from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from .views import HomeRUDView, HomeAPIView, HomeListView, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet)


urlpatterns = [
    path('home/', HomeAPIView.as_view()),  # add a new project
    path('home/all/', HomeListView.as_view()),  # get all projects
    path('home/<int:id>', HomeRUDView.as_view()),  # id here stands for the id of the project
    url('users/', include(router.urls)),  # get all users
    url(r'^auth/', include('rest_auth.urls')),
]
