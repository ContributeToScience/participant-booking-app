from tastypie.constants import ALL
from tastypie.exceptions import Unauthorized
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.throttle import CacheThrottle

from scientist.models import Research


class ResearchAuthorization(Authorization):
    '''
    Uses permission checking from ``django.contrib.auth`` to map
    ``POST / PUT / DELETE / PATCH`` to their equivalent Django auth
    permissions.

    Both the list & detail variants simply check the model they're based
    on, as that's all the more granular Django's permission setup gets.
    '''

    def base_checks(self, request, model_klass):
        # If it doesn't look like a model, we can't check permissions.
        if not model_klass or not getattr(model_klass, '_meta', None):
            return False

        # User must be logged in to check permissions.
        if not hasattr(request, 'user'):
            return False

        return model_klass

    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)

        if klass is False:
            return []

        object_list = object_list.filter(researcher=bundle.request.user).order_by('-created')

        # GET-style methods are always allowed.
        return object_list

    def read_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        if not bundle.obj.researcher == bundle.request.user:
            raise Unauthorized('You are not allowed to access that resource.')

        # GET-style methods are always allowed.
        return True

    def create_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        return True

    def update_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        if not bundle.obj.researcher == bundle.request.user:
            raise Unauthorized('You are not allowed to access that resource.')

        return True

    def delete_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized('You are not allowed to access that resource.')

        if not bundle.obj.researcher == bundle.request.user:
            raise Unauthorized('You are not allowed to access that resource.')

        return True


class ResearchResource(ModelResource):
    class Meta:
        always_return_data = True
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        list_allowed_methods = ['get', 'post']
        resource_name = 'research'
        queryset = Research.objects.all().order_by('-created')
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = ResearchAuthorization()
        filtering = {
            'start': ('exact', 'lt', 'lte', 'gte', 'gt'),
            'end': ('exact', 'lt', 'lte', 'gte', 'gt'),
            'scientist': ALL,
        }
        ordering = ['-created']
        throttle = CacheThrottle(throttle_at=600)

    def determine_format(self, request):
        '''Return JSON by default'''
        return 'application/json'
