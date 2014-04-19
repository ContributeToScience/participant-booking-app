from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       # avatar urls
                       url(r'^avatar/upload/$', 'core.views.upload_avatar', name='upload_avatar'),
                       url(r'^$', 'core.views.home', name='home'),
                       url(r'^socialaccount/signup/success/$', 'core.views.signup_success', name='signup_success'),
)