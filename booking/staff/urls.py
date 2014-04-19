from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^staff/award/participants/$', 'staff.views.award_participants', name='award_participants'),
                       url(r'^staff/award/participants/history/$', 'staff.views.award_participants_history',
                           name='award_participants_history'),
                       url(r'^staff/scientists/payment/history/$', 'staff.views.scientists_payment_history',
                           name='scientists_payment_history'),
                       url(r'^staff/payment/paypal/complete/$', 'staff.views.payment_paypal_complete',
                           name='payment_paypal_complete'),
)