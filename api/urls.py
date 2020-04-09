from django.urls import path, include
from api.views import HomeRUDView, HomeAPIView, HomeListView, CreateUserViewSet, GetAllUsersViewSet, GetUserViewSet

urlpatterns = [
    path('home/', HomeAPIView.as_view()),                                # add a new project
    path('home/all/', HomeListView.as_view()),                           # get all projects
    path('home/<int:id>', HomeRUDView.as_view()),                        # id here stands for the id of the project
    path('users/', CreateUserViewSet.as_view(), name='create_user'),     # get all users
    path('users/all/', GetAllUsersViewSet.as_view(), name='all_users'),  # get all users
    path('users/<int:pk>', GetUserViewSet.as_view(), name='get_user'),   # get a specific users
    path('auth/', include('rest_auth.urls')),       # DRF auth system
]
