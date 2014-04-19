from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from tastypie.utils import trailing_slash
from tastypie.http import HttpForbidden, HttpUnauthorized
from tastypie.models import ApiKey
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.resources import ModelResource


class UserResource(ModelResource):
    class Meta:
        always_return_data = True
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        list_allowed_methods = ['get', 'post']
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        excludes = ['objects', 'is_active', 'is_staff', 'is_superuser', 'password']

    def determine_format(self, request):
        """Return JSON by default"""
        return 'application/json'

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.raw_post_data,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username_or_email = data.get('username_or_email', '')
        password = data.get('password', '')

        user = authenticate(username=username_or_email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                bundle = self.build_bundle(obj=user, request=request)
                bundle = self.full_dehydrate(bundle)
                # Only return apikey in login api
                apikey = None
                try:
                    apikey = ApiKey.objects.get(user=request.user)
                except:
                    pass

                bundle.data['apikey'] = apikey
                bundle = self.alter_detail_data_to_serialize(request, bundle)
                return self.create_response(request, bundle)

            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            user = authenticate(email=username_or_email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    bundle = self.build_bundle(obj=user, request=request)
                    bundle = self.full_dehydrate(bundle)
                    bundle = self.alter_detail_data_to_serialize(request, bundle)
                    return self.create_response(request, bundle)

                else:
                    return self.create_response(request, {
                        'success': False,
                        'reason': 'disabled',
                    }, HttpForbidden)
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)
