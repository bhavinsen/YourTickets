from django.conf.urls import url

from . import views

urlpatterns = [
    # called after mollie payment, was paymentDone, 205, 5634
    url(r'^buy/(?P<order_id>.+)/(?P<event_id>.+)$', views.thank_you, name='buy_ticket_mollie'),
    url(r'^buy/(?P<order_id>.+)$', views.thank_you, name='buy_ticket_mollie'),

    # this page also calculated the max sold
    # url(r'^(?P<event_id>[-\w.]+)/(?P<event_name>.+)/(?P<channel_url_name>.+)/$', views.index, name='buy_ticket'),
    url(r'^(?P<event_id>[-\w.]+)/(?P<event_name>.+)/(?P<channel_url_name>.+)/soldout/(?P<some_tickets_soldout>.+)$',views.index, name='buy_ticket'),
    url(r'^(?P<event_id>[-\w.]+)/(?P<event_name>.+)/(?P<channel_url_name>.+)/$', views.index, name='buy_ticket'),
    url(r'^(?P<event_id>.+)/(?P<event_name>.+)/soldout/(?P<some_tickets_soldout>.+)/$', views.index, name='buy_ticket'),

    url(r'^(?P<event_id>.+)/(?P<event_name>.+)/$', views.index, name='buy_ticket'),
    url(r'^(?P<event_id>.+)/(?P<event_name>.+)/ticket_overview$', views.ticket_overview, name='ticketshop_ticket_overview'),

    # final step in order process
    url(r'^(?P<event_id>.+)/(?P<event_name>.+)/pay$', views.pay, name='confirm_ticket'),
    url(r'^guestlist/profile/(?P<hash>[-\w\.]+)$', views.guestlist_profile, name='guestlist_profile'),

    # this could be deleted i think
    url(r'^guestlist/thankyou/(?P<hash>[-\w\.]+)$', views.guestlist_thankyou, name='guestlist_thankyou'),

    url(r'^multi/(?P<multiticketshop_id>.+)$', views.multiticketshop, name='multiticketshop')

]
