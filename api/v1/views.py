from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from api.models import PreviousProject, User
from .serializers import PreviousProjectSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class HomeListView(generics.ListAPIView):
    serializer_class = PreviousProjectSerializer
    queryset = PreviousProject.objects.all()
    permission_classes = [IsAuthenticated | ReadOnly]


class HomeAPIView(generics.CreateAPIView):
    serializer_class = PreviousProjectSerializer

    def post(self, request, *args, **kwargs):
        res = self.create(request, *args, **kwargs)
        content = {
            'data': {
                'id': res.data.get('id'),
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'githubURL': request.POST.get('githubURL'),
                'imageURL': request.POST.get('imageURL'),
                'tags': request.POST.get('tags'),
                'likes': request.POST.get('likes'),
                'pub_date': request.POST.get('pub_date'),
            },
            'msg': 'project created successfully',
            'status': res.status_code
        }
        return Response(content)


class HomeRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = PreviousProjectSerializer
    queryset = PreviousProject.objects.all()
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, *args, **kwargs):
        content = {}
        try:
            res = self.retrieve(request, *args, **kwargs)
            content['data'] = {
                'id': res.data.get('id'),
                'title': res.data.get('title'),
                'content': res.data.get('content'),
                'githubURL': res.data.get('githubURL'),
                'imageURL': res.data.get('imageURL'),
                'tags': res.data.get('tags'),
                'likes': res.data.get('likes'),
                'pub_date': res.data.get('pub_date'),
            }
            content['msg'] = 'element retrieved successfully'
            content['status'] = res.status_code
        except Http404 as e:
            print(e)
            content['msg'] = 'element not found'
            content['status'] = 404
        return Response(content)


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = PreviousProjectSerializer

    def post(self, request, *args, **kwargs):
        res = self.create(request, *args, **kwargs)
        content = {
            'data': {
                'id': res.data.get('id'),
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'githubURL': request.POST.get('githubURL'),
                'imageURL': request.POST.get('imageURL'),
                'tags': request.POST.get('tags'),
                'likes': request.POST.get('likes'),
                'pub_date': request.POST.get('pub_date'),
            },
            'msg': 'project created successfully',
            'status': res.status_code
        }
        return Response(content)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
