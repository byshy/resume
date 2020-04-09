from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import PreviousProject, User
from api.serializers import PreviousProjectSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser, ReadOnly
from django.utils import timezone


class HomeListView(generics.ListAPIView):
    serializer_class = PreviousProjectSerializer
    queryset = PreviousProject.objects.filter(
        pub_date__lte=timezone.now()
    )
    permission_classes = [IsAuthenticated | ReadOnly]


# get all previous projects


class HomeAPIView(generics.CreateAPIView):
    serializer_class = PreviousProjectSerializer

    def post(self, request, *args, **kwargs):
        serializer = PreviousProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'data': serializer.data,
                'msg': 'project created successfully',
                'status': status.HTTP_201_CREATED
            }
            return Response(content)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create a new project


class HomeRUDView(APIView):
    permission_classes = [IsLoggedInUserOrAdmin]

    def get_object(self, id):
        try:
            return PreviousProject.objects.get(id=id)
        except PreviousProject.DoesNotExist:
            raise Http404

    def get(self, request, id):
        try:
            pp = self.get_object(id)
            serializer = PreviousProjectSerializer(pp)
            content = {
                'data': serializer.data,
                'msg': 'element retrieved successfully',
                'status': status.HTTP_200_OK
            }
            return Response(content)
        except Http404:
            return Response({'msg': 'element not found', 'status': status.HTTP_404_NOT_FOUND})


# get a specific project


class GetAllUsersViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]


# get all users


class CreateUserViewSet(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'data': {
                    'pk': serializer.data.get('pk'),
                    'email': serializer.data.get('email'),
                    'first_name': serializer.data.get('first_name'),
                    'last_name': serializer.data.get('last_name'),
                    'profile': {
                        "mobile": serializer.data.get('profile')["mobile"]
                    },
                },
                'msg': 'account created successfully',
                'status': status.HTTP_201_CREATED
            }
            return Response(content)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create a new user account


class GetUserViewSet(APIView):
    permission_classes = [IsAdminUser, ]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            user = self.get_object(pk)
            serializer = UserSerializer(user)
            content = {
                'data': serializer.data,
                'msg': 'element retrieved successfully',
                'status': status.HTTP_200_OK
            }
            return Response(content)
        except Http404:
            return Response({'msg': 'element not found', 'status': status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)


# get a specific user
