from tastypie.authorization import Authorization

from .models import PreviousProject, UserProfile
from tastypie.resources import ModelResource


class PPResource(ModelResource):
    class Meta:
        queryset = PreviousProject.objects.all()
        resource_name = 'PreviousProject'
        authorization = Authorization()
        always_return_data = True


class UserResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'UserProfile'
        authorization = Authorization()
        always_return_data = True
