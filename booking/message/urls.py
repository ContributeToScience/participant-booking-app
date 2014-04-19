from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^message/post/$', 'message.views.message_post', name='message_post'),
                       url(r'^message/(?P<message_id>\d+)/detail/$', 'message.views.message_detail',
                           name='message_detail'),
                       url(r'^message/delete/$', 'message.views.message_delete', name='message_delete'),
                       url(r'^message/undo/$', 'message.views.message_undo', name='message_undo'),
                       url(r'^message/list/(?P<message_flag>\w+)/$', 'message.views.message_list', name='message_list'),
)