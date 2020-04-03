from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import PreviousProject, User
from api.serializers import PreviousProjectSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser, ReadOnly


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
    permission_classes = [IsLoggedInUserOrAdmin]

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


class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AllUsersViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetUser(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        content = {}
        try:
            res = self.retrieve(request, *args, **kwargs)
            content['data'] = {
                'pk': res.data.get('pk'),
                'email': res.data.get('email'),
                'first_name': res.data.get('first_name'),
                'last_name': res.data.get('last_name'),
                'mobile': res.data.get('profile')['mobile'],
            }
            content['msg'] = 'element retrieved successfully'
            content['status'] = res.status_code
        except Http404 as e:
            print(e)
            content['msg'] = 'element not found'
            content['status'] = 404
        return Response(content)
