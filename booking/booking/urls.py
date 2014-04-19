from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'', include('participant.urls')),
                       url(r'', include('scientist.urls')),
                       url(r'', include('department.urls')),
                       url(r'', include('rating.urls')),
                       url(r'', include('core.urls')),
                       url(r'', include('staff.urls')),
                       url(r'', include('message.urls')),
                       url(r'^u/', include('userprofile.urls')),
                       #url(r'^api/', include('api.urls')),

                       url(r'^userrole/$', 'userprofile.views.userrole', name='userrole'),
                       url(r'^userrole/switch/(?P<user_type>\w+)/$', 'userprofile.views.switch_userrole', name='switch_userrole'),

                       url(r'^account/$', 'userprofile.views.account', name='account'),
                       url(r'^userrole/delete/(?P<user_type>\w+)/$', 'userprofile.views.delete_account', name='delete_account'),

                       url(r'^accounts/signup/', TemplateView.as_view(template_name='home.html'),
                           name='account_signup'),
                       url(r'^accounts/login/', 'userprofile.views.login', name='account_login'),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^accounts/ajax/login/', 'userprofile.views.ajax_login', name='account_ajax_login'),
                       url(r'^accounts/ajax/signup/', 'userprofile.views.ajax_signup', name='account_ajax_signup'),
                       url(r'^accounts/ajax/login_signup/', 'userprofile.views.ajax_login_signup', name='ajax_login_signup'),

                       url(r'^payment/paypal/ipn/', include('paypal.standard.ipn.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^robots.txt', TemplateView.as_view(template_name='robots.txt')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }),
    )

urlpatterns += patterns('django.contrib.flatpages.views',
                        (r'^page/(?P<url>.*)$', 'flatpage'),
)