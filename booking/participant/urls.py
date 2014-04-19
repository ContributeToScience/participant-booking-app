from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from userprofile.views import USER_TYPE_PARTICIPANT
from .forms import ParticipantBasicInfoForm, ParticipantQuestionForm

urlpatterns = patterns('',
                       url(r'^participant/$', 'participant.views.participant', name='participant'),
                       url(r'^participant/basicinfo/$', 'userprofile.views.userprofile_basic_info',
                           name='participant_basic_info',
                           kwargs={
                               'form_class': ParticipantBasicInfoForm,
                               'success_url': reverse_lazy('participant_questions'),
                               'user_type': USER_TYPE_PARTICIPANT,
                               'template': 'userprofile/basic_info.html',
                           }
                       ),
                       url(r'^participant/questions/$', 'userprofile.views.userprofile_questions',
                           name='participant_questions',
                           kwargs={
                               'form_class': ParticipantQuestionForm,
                               'success_url': reverse_lazy('participant'),
                               'user_type': USER_TYPE_PARTICIPANT,
                               'template': 'userprofile/questions.html',
                           }
                       ),
                       url(r'^participant/signup/$', 'userprofile.views.participant_signup', name='participant_signup',
                           kwargs={
                               'success_url': reverse_lazy('participant_basic_info'),
                               'user_type': USER_TYPE_PARTICIPANT,
                           }
                       ),
                       url(r'^participant/research/(?P<research_id>\d+)/$', 'participant.views.research_detail',
                           name='participant_research_detail'),
                       url(r'^participant/research/(?P<research_id>\d+)/modal/$', 'participant.views.research_detail',
                           name='participant_research_detail_modal',
                           kwargs={
                               'template': 'participant/research_detail_modal.html',
                           }),
                       url(r'^participant/take_part_researches/$', 'participant.views.take_part_researches',
                           name='take_part_researches'),
                       url(r'^participant/take_part_researches_calendar/$',
                           'participant.views.take_part_researches_calendar', name='take_part_researches_calendar'),
                       url(r'^api/participant/events/$', 'participant.views.api_participant_events',
                           name='api_participant_events'),
                       url(r'^participant/take_part_event/$', 'participant.views.take_part_event',
                           name='take_part_event'),
                       url(r'^participant/take_part_credit_schemes/$', 'participant.views.take_part_credit_schemes',
                           name='take_part_credit_schemes'),
                       url(r'^participant/payment/messages/$', 'participant.views.payment_messages',
                           name='payment_messages'),
                       url(r'^participant/get_payment_info/$', 'participant.views.get_payment_info',
                           name='get_payment_info'),
                       # url(r'^participant/send_notification_test/(?P<type>[-\w]+)/$',
                       #     'participant.views.send_notification_test', name='send_notification_test'),
                       url(r'^participant/research_list/(?P<study_type>\w+)/$', 'participant.views.research_list',
                           name='research_list'),
)