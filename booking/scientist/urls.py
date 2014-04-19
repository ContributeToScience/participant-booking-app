from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from userprofile.views import USER_TYPE_SCIENTIST
from .forms import ScientistBasicInfoForm

urlpatterns = patterns('',
                       url(r'^scientist/$', 'scientist.views.scientist', name='scientist'),
                       url(r'^scientist/signup/$', 'userprofile.views.scientist_signup', name='scientist_signup',
                           kwargs={
                               'success_url': reverse_lazy('scientist_basic_info'),
                               'user_type': USER_TYPE_SCIENTIST,
                           }
                       ),
                       url(r'^scientist/basicinfo/$', 'userprofile.views.userprofile_basic_info',
                           name='scientist_basic_info',
                           kwargs={
                               'form_class': ScientistBasicInfoForm,
                               'success_url': reverse_lazy('scientist'),
                               'user_type': USER_TYPE_SCIENTIST,
                               'template': 'userprofile/basic_info.html',
                           }
                       ),
                       url(r'^scientist/research/add/$', 'scientist.views.scientist_research_post',
                           name='scientist_research_add'),
                       url(r'^scientist/research/(?P<research_id>\d+)/edit/$',
                           'scientist.views.scientist_research_post',
                           name='scientist_research_edit'),
                       url(r'^scientist/research/$', 'scientist.views.scientist_research_list',
                           name='scientist_research_list'),
                       url(r'^scientist/update_publish_status/$', 'scientist.views.update_publish_status',
                           name='update_publish_status'),
                       url(r'^scientist/research/(?P<research_id>\d+)/copy/$', 'scientist.views.research_copy',
                           name='research_copy'),
                       url(r'^scientist/research/delete/$', 'scientist.views.research_delete',
                           name='research_delete'),
                       url(r'^scientist/research/(?P<research_id>\d+)/detail/$', 'scientist.views.research_detail',
                           name='research_detail'),
                       url(r'^scientist/research/confirmed_participant/$', 'scientist.views.confirmed_participant',
                           name='confirmed_participant'),
                       url(r'^scientist/research/reject_participant/$', 'scientist.views.reject_participant',
                           name='reject_participant'),
                       url(r'^scientist/research/assign_credit/$', 'scientist.views.assign_credit',
                           name='assign_credit'),
                       url(r'^scientist/scheme_list/$', 'scientist.views.scientist_scheme_list',
                           name='scientist_scheme_list'),
                       url(r'^scientist/scheme/(?P<scheme_id>\d+)/detail/$', 'scientist.views.scientist_scheme_detail',
                           name='scientist_scheme_detail'),
                       url(r'^scientist/scheme/assign_credit/$', 'scientist.views.scheme_assign_credit',
                           name='scheme_assign_credit'),
                       url(r'^api/scientist/events/$', 'scientist.views.api_scientist_events',
                           name='api_scientist_events'),
                       url(r'^scientist/research/(?P<research_id>\d+)/events/$', 'scientist.views.research_event_list',
                           name='research_event_list'),
                       url(r'^scientist/research/create_event/$', 'scientist.views.create_research_event',
                           name='create_research_event'),
                       url(r'^scientist/research/delete_event/$', 'scientist.views.delete_research_event',
                           name='delete_research_event'),
                       url(r'^scientist/research/copy_event/$', 'scientist.views.copy_research_event',
                           name='copy_research_event'),
                       url(r'^scientist/research/get_event/$', 'scientist.views.get_research_event',
                           name='get_research_event'),
                       url(r'^scientist/research/event/(?P<event_id>\d+)/participants/$',
                           'scientist.views.event_participant_list',
                           name='event_participant_list'),
                       url(r'^scientist/research/resize_event/$', 'scientist.views.resize_research_event',
                           name='resize_research_event'),

                       url(r'^scientist/research/(?P<research_id>\d+)/payment/paypal/$',
                           'scientist.views.scientist_research_payment_paypal',
                           name='scientist_research_payment_paypal'),

                       url(r'^scientist/research/(?P<research_id>\d+)/payment/paypal/complete/$',
                           'scientist.views.research_paypal_complete',
                           name='research_paypal_complete'),

                       url(r'^scientist/research/(?P<research_id>\d+)/payment/amazon/$',
                           'scientist.views.scientist_research_payment_amazon',
                           name='scientist_research_payment_amazon'),
                       url(r'^scientist/research/update_duration/$', 'scientist.views.update_research_duration',
                           name='update_research_duration'),
                       url(r'^scientist/research/(?P<research_id>\d+)/complete/$',
                           'scientist.views.update_complete_status', name='update_complete_status'),
                       url(r'^scientist/payment/record/$', 'scientist.views.scientist_payment_record',
                           name='scientist_payment_record'),
                       url(r'^scientist/anonymous/donate/paypal/complete/$',
                           'scientist.views.anonymous_donate_paypal_complete', name='anonymous_donate_paypal_complete'),

                       url(r'^scientist/research/(?P<research_id>\d+)/payment/fake/$',
                           'scientist.views.scientist_research_payment_fake',
                           name='scientist_research_payment_fake'),
)