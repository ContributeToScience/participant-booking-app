from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^rating/get_scientist_score/$', 'rating.views.get_scientist_score',
                           name='get_scientist_score'),
                       url(r'^rating/set_scientist_score/$', 'rating.views.set_scientist_score',
                           name='set_scientist_score'),
                       url(r'^rating/get_participant_score/$', 'rating.views.get_participant_score',
                           name='get_participant_score'),
                       url(r'^rating/set_participant_score/$', 'rating.views.set_participant_score',
                           name='set_participant_score'),
)