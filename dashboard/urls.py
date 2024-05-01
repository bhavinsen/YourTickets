from django.conf.urls import url, include

from dashboard.views.event import general, tickettypes, lineup, bankaccount, ticketshop_design
from dashboard.views import statistics
from dashboard.views import visitors
from dashboard.views import events
from dashboard.views import main_dashboard
from dashboard.views import multi_ticketshop
from dashboard.views import sales_channels
from dashboard.views import share_event


urlpatterns = [
    url(r'^$', main_dashboard.index, name='dashboard_index'),
    url(r'^gettoken$', main_dashboard.gettoken, name='dashboard_gettoken'),
    url(r'^createevent/completed/(?P<event_id>[-\w\.]*)/$', events.event_new_completed, name='event_new_completed'),
    url(r'^createevent/$', events.event_new, name='event_new'),

    url(r'^multi_ticketshop/$', multi_ticketshop.index, name='dashboard_multiticketshop'),
    url(r'^multi_ticketshop/create$', multi_ticketshop.create_ticketshop, name='dashboard_multiticketshop_create'),
    url(r'^multi_ticketshop/(?P<multishop_id>[0-9]+)/edit$', multi_ticketshop.edit_ticketshop, name='dashboard_multiticketshop_edit'),
    url(r'^multi_ticketshop/(?P<multishop_id>[0-9]+)/delete$', multi_ticketshop.delete_ticketshop, name='dashboard_multiticketshop_delete'),
    url(r'^multi_ticketshop/(?P<multishop_id>[-\w\.]*)/request_url', multi_ticketshop.request_short_url, name='dashboard_multiticketshop_request_short'),
    url(r'^multi_ticketshop/(?P<multishop_id>[-\w\.]*)/edit/events_list/(?P<list_type>[-\w\.]*)', multi_ticketshop.events_list, name='dashboard_multiticketshop_edit_event_list'),
    url(r'^multi_ticketshop/(?P<multishop_id>[-\w\.]*)/edit/position/(?P<position>[-\w\.]*)/(?P<linked_event_id>[-\w\.]*)', multi_ticketshop.event_position, name='dashboard_multiticketshop_edit_event_position'),
    url(r'^multi_ticketshop/(?P<multishop_id>[-\w\.]*)/edit/delete/(?P<linked_event_id>[-\w\.]*)', multi_ticketshop.delete_event, name='dashboard_multiticketshop_edit_event_delete'),
    url(r'^multi_ticketshop/(?P<multishop_id>[-\w\.]*)/edit/add/(?P<event_id>[-\w\.]*)/(?P<position>[-\w\.]*)', multi_ticketshop.add_event, name='dashboard_multiticketshop_edit_event_add'),
    url(r'^multi_ticketshop/(?P<multishop_id>[-\w\.]*)/update', multi_ticketshop.update_ticketshop, name='dashboard_multiticketshop_update'),

    url(r'^(?P<event_id>[0-9]+)/statistics/chart_revenue$', statistics.chart_revenue, name='dashboard_statistics_chart_revenue'),
    # url(r'^(?P<event_id>[0-9]+)/statistics/chart_data$', statistics.chart_data, name='dashboard_statistics_chart_data'),
    url(r'^(?P<event_id>[0-9]+)/statistics/$', statistics.index, name='dashboard_statistics'),


    url(r'^(?P<event_id>[0-9]+)/', include(([
        url(r'^sales_channels/', include(([
            url(r'^$', sales_channels.index, name='index'),
            url(r'^create$', sales_channels.create, name='create'),
            url(r'^(?P<channel_id>[-\w.]+)/edit$', sales_channels.edit, name='edit'),
            url(r'^(?P<channel_id>[-\w.]+)/delete$', sales_channels.delete, name='delete'),
        ], 'sales_channels'))),
        url(r'^share_event/', include(([
            url(r'^$', share_event.index, name='index'),
            url(r'^create$', share_event.create, name='create'),
            url(r'^(?P<id>[-\w\.]+)/delete/(?P<type>[-\w\.]+)$', share_event.delete, name='delete'),
        ], 'share_event'))),
    ], 'dashboard_event'))),

    url(r'^(?P<event_id>[0-9]+)/delete/$', general.event_delete, name='dashboard_event_delete'),
    url(r'^(?P<event_id>[0-9]+)/edit/algemeen/$', general.edit_algemeen, name='dashboard_event_general'),
    url(r'^(?P<event_id>[0-9]+)/edit/tickets/$', tickettypes.index, name='dashboard_event_tickets'),
    url(r'^(?P<event_id>[0-9]+)/edit/tickets/remove/(?P<item_id>[0-9]+)$', tickettypes.remove_item, name='dashboard_event_tickets_remove'),
    url(r'^(?P<event_id>[0-9]+)/edit/tickets/add$', tickettypes.add_item, name='dashboard_event_tickets_add'),
    url(r'^(?P<event_id>[0-9]+)/edit/lineup/$', lineup.index, name='dashboard_event_lineup'),
    url(r'^(?P<event_id>[0-9]+)/edit/lineup/remove/(?P<item_id>[0-9]+)$', lineup.remove_item, name='dashboard_event_lineup_remove'),
    url(r'^(?P<event_id>[0-9]+)/edit/lineup/add$', lineup.add_item, name='dashboard_event_lineup_add'),
    url(r'^(?P<event_id>[0-9]+)/edit/bank/$', bankaccount.index, name='dashboard_event_bank'),
    url(r'^(?P<event_id>[0-9]+)/edit/ticketshop/$', ticketshop_design.index, name='dashboard_event_ticketshop_design'),
    url(r'^(?P<event_id>[0-9]+)/edit/changelive/$', general.change_live, name='dashboard_event_changelive'),

    #visitors
    url(r'^(?P<event_id>[0-9]+)/visitors/$', visitors.index, name='dashboard_visitors'),
    url(r'^(?P<event_id>[0-9]+)/visitors/(?P<ticket_id>[-\w\.]+)$', visitors.ajax_get_visitors_for_ticket, name='dashboard_visitors_getlist'),
    url(r'^(?P<event_id>[0-9]+)/visitors/(?P<ticket_id>[-\w\.]+)/download$', visitors.download_visitors_per_ticket, name='dashboard_visitors_download_per_ticket'),
    url(r'^(?P<event_id>[0-9]+)/visitors/guestlist/upload', visitors.visitors_upload, name='dashboard_visitors_guestlist_upload'),
    url(r'^(?P<event_id>[0-9]+)/visitors/guestlist/send', visitors.visitors_send, name='dashboard_visitors_guestlist_send'),
    url(r'^ajaxticket/(?P<ticket_id>[-\w\.]+)/delete$', visitors.ajax_delete_ticket, name='dashboard_visitors_ticket_delete'),
    # this url is actually not used
    url(r'^(?P<event_id>[0-9]+)/visitors/downloadVisitorlog/$', visitors.downloadVisitorlog),

]
