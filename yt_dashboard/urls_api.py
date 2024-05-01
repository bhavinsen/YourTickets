from django.conf.urls import url, include
from django.urls import path, re_path

from yt_dashboard.views.api.account import aggregate
from yt_dashboard.views.api.event import stats as event_stats, index as event, saleschannels, visitors
from yt_dashboard.views.api import multiticketshop
from yt_dashboard.views.api import stats

app_name = 'api'

urlpatterns = [

    path('multiticketshop/', include([
        path('getall', multiticketshop.getall),
        path('getevents', multiticketshop.get_events_from_user),
        path('create', multiticketshop.create),
        path('<int:multiticketshop_id>/getevents', multiticketshop.get_events_for_shop),
        path('<int:multiticketshop_id>/update', multiticketshop.update),
        path('<int:multiticketshop_id>/delete', multiticketshop.delete),
        path('<int:multiticketshop_id>/request', multiticketshop.request_short_url),
    ])),

    url(r'^event/getall$', event.getall, name='event_getall'),
    url(r'^event/search/(?P<title_filter>[-\w\.]+)$', event.search, name='event_search'),
    url(r'^event/search/$', event.search, name='event_search'),
    url(r'^event/get/(?P<id>[-\w\.]+)$', event.get, name='event_get'),
    url(r'^event/create$', event.create, name='event_create'),
    path('event/delete/<int:id>', event.delete),


    url(r'^event/(?P<id>[-\w\.]+)/', include(([

        url(r'^sales_channels/', include(([
            url(r'^getall$', saleschannels.getall, name='event_saleschannels_getall'),
            url(r'^create$', saleschannels.create, name='event_saleschannels_create'),
            url(r'^(?P<saleschannel_id>[-\w\.]+)/update$', saleschannels.update, name='event_saleschannels_update'),
            url(r'^(?P<saleschannel_id>[-\w\.]+)/delete$', saleschannels.delete, name='event_saleschannels_delete'),
        ], 'api_event_saleschannels'))),

        path('publish', event.publish),
        path('unpublish', event.unpublish),
        path('can_be_published', event.check_publish),


        # form some reason this was sales_channels
        path('visitors/', include([
            path('get_event_tickets', visitors.get_event_tickets),
            path('visitors_for_ticket/<str:ticket_id>', visitors.get_visitors_for_ticket),
            # path('upload', visitors.visitors_upload),
            # path('send', visitors.visitors_send),
            path('deleteticket', visitors.delete_ticket),
            path('send_single_ticket', visitors.send_single_ticket),
            path('download', visitors.downloadVisitors),
            path('download/<str:ticket_id>', visitors.downloadVisitorsPerTicket)
        ])),

        path('stats/', include([
            path('sold_ticket_amount/<str:date_from>/<str:date_till>', event_stats.sold_ticket_amount),
            path('sold_ticket_amount', event_stats.sold_ticket_amount),

            path('revenue/<str:date_from>/<str:date_till>', event_stats.revenue),
            path('revenue', event_stats.revenue),

            path('visitors/<str:date_from>/<str:date_till>', event_stats.visitors),
            path('visitors', event_stats.visitors),

            path('conversion_rate/<str:date_from>/<str:date_till>', event_stats.conversion_rate),
            path('conversion_rate', event_stats.conversion_rate),

            path('gender_chart/<str:date_from>/<str:date_till>', event_stats.gender_chart),
            path('gender_chart', event_stats.gender_chart),

            path('ticketscount/<str:date_from>/<str:date_till>', event_stats.ticketscount),
            path('ticketscount', event_stats.ticketscount),

            path('age_and_gender/<str:date_from>/<str:date_till>', event_stats.age_and_gender),
            path('age_and_gender', event_stats.age_and_gender),

            path('get_earnings_chart/<str:date_from>/<str:date_till>', event_stats.earnings_chart),
            path('get_earnings_chart', event_stats.earnings_chart),

            path('list_residence/<str:date_from>/<str:date_till>', event_stats.list_residence),
            path('list_residence', event_stats.list_residence),

            path('total_sold_of/<str:date_from>/<str:date_till>', event_stats.total_sold_of),
            path('total_sold_of', event_stats.total_sold_of),

            path('new_vs_returning_visitors/<str:date_from>/<str:date_till>', event_stats.new_vs_returning_visitors),
            path('new_vs_returning_visitors', event_stats.new_vs_returning_visitors),
        ])),


    ], 'api_event'))),

    path('stats/', include([
        path('get_gender_chart/<str:date_from>/<str:date_till>', stats.get_gender_chart),
        path('get_top_5_chart/<str:chart_type>/<str:date_from>/<str:date_till>', stats.get_top_5_chart),
        path('get_earnings_chart/<str:chart_type>/<str:date_from>/<str:date_till>', stats.get_earnings_chart),
        path('get_ticketscount/<str:date_from>/<str:date_till>', stats.get_ticketscount),
        path('new_vs_returning_visitors/<str:date_from>/<str:date_till>', stats.new_vs_returning_visitors),
        path('list_residence/<str:date_from>/<str:date_till>', stats.list_residence),
        path('age_gender/<str:date_from>/<str:date_till>', stats.age_gender),



        path('aggregate/sold_ticket_amount/<str:date_from>/<str:date_till>', aggregate.sold_ticket_amount),
        path('aggregate/revenue/<str:date_from>/<str:date_till>', aggregate.revenue),
        path('aggregate/visitors/<str:date_from>/<str:date_till>', aggregate.visitors),
        path('aggregate/conversion_rate/<str:date_from>/<str:date_till>', aggregate.conversion_rate),

    ])),

]

