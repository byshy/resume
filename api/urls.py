from django.urls import path, include
from api.views import HomeRUDView, HomeAPIView, HomeListView, UserViewSet, AllUsersViewSet, GetUser

urlpatterns = [
    path('home/', HomeAPIView.as_view()),           # add a new project
    path('home/all/', HomeListView.as_view()),      # get all projects
    path('home/<int:id>', HomeRUDView.as_view()),   # id here stands for the id of the project
    path('users/', UserViewSet.as_view()),          # get all users
    path('users/all/', AllUsersViewSet.as_view()),  # get all users
    path('users/<int:pk>', GetUser.as_view()),      # get a specific users
    path('auth/', include('rest_auth.urls')),       # DRF auth system
]
