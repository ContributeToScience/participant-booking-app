from django.conf.urls import patterns, url

urlpatterns = patterns('userprofile.views',
                       url(r'^(?P<username>[\w.@+-]+)/$', 'userprofile', name='userprofile'),
                       url(r'^(?P<username>[\w.@+-]+)/basic_info/$', 'basic_info', name='basic_info'),
                       url(r'^(?P<username>[\w.@+-]+)/question_info/$', 'question_info', name='question_info'),
)