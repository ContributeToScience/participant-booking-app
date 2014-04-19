from django.conf.urls import patterns, url, include
from tastypie.api import Api

from .resources.user import UserResource
from .resources.research import ResearchResource

api = Api()
api.register(UserResource())
api.register(ResearchResource())

urlpatterns = patterns('',
                       url(r'', include(api.urls)),
)