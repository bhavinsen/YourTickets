from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    base,
    users,
    orders,
    dashboard,
    translations,
    cashflow,
    content,
    financial,
    guestlist,
    events
)

urlpatterns = [
    url(r'^$', base.index, name='youradmin'),
    url(r'^login', LoginView.as_view(template_name= 'youradmin/login.html'), name='youradmin_login'),
    url(r'^logout', LogoutView.as_view(next_page= '/'), name='youradmin_logout'),

    #users
    url(r'^users/$', users.index, name='youradmin_users_index'),
    url(r'^users/getlist', users.getlist, name='youradmin_users_getlist'),
    url(r'^users/delete/(?P<user_id>[-\w\.]+)$', users.delete, name='youradmin_users_delete'),
    url(r'^users/(?P<user_id>[-\w\.]+)/orders$', users.orders, name='youradmin_users_orders'),
    url(r'^users/(?P<user_id>[-\w\.]+)/orders/getlist$', users.get_orders_list, name='youradmin_users_orders_getlist'),

    url(r'^users/(?P<user_id>[-\w\.]+)/order/(?P<order_id>[-\w\.]+)/tickets$', users.get_tickets_for_order, name='youradmin_users_orders_tickets'),
    url(r'^users/(?P<user_id>[-\w\.]+)/order/(?P<order_id>[-\w\.]+)/tickets/getlist$', users.get_tickets_for_order_list, name='youradmin_users_orders_tickets_getlist'),

    # orders
    url(r'^orders/$', orders.dashboard, name='youradmin_orders_dashboard'),
    url(r'^orders/list$', orders.orderlist, name='youradmin_orders_list'),
    url(r'^orders/getlist$', orders.getlist, name='youradmin_orders_getlist'),

    url(r'^orders/delete/(?P<order_id>[-\w\.]+)$', orders.delete, name='youradmin_orders_delete'),
    url(r'^orders/send/(?P<order_id>[-\w\.]+)$', orders.send, name='youradmin_orders_send'),

    # translations
    url(r'^translations$', translations.index, name='youradmin_translations'),

    url(r'^translations/create/(?P<language_id>[-\w\.]+)$', translations.create_translations, name='youradmin_translations_create'),
    url(r'^translations/(?P<translation_id>[-\w\.]+)/edit$', translations.translation_edit, name='youradmin_translations_edit'),
    url(r'^translations/(?P<translation_id>[-\w\.]+)/delete$', translations.translation_delete, name='youradmin_translations_delete'),


    url(r'^translations/getlist$', translations.getlist, name='youradmin_translations_getlist'),
    url(r'^translations/getlist/(?P<language_id>[-\w\.]+)$', translations.getlist, name='youradmin_translations_getlist'),

    url(r'^translations/languages$', translations.language_index, name='youradmin_translations_languages'),
    url(r'^translations/languages/getlist$', translations.language_getlist, name='youradmin_translations_languages_getlist'),
    url(r'^translations/languages/create$', translations.language_create, name='youradmin_translations_languages_create'),
    url(r'^translations/languages/(?P<language_id>[-\w\.]+)/edit$', translations.language_edit, name='youradmin_translations_languages_edit'),
    url(r'^translations/languages/(?P<language_id>[-\w\.]+)/delete', translations.language_delete, name='youradmin_translations_languages_delete'),
    url(r'^translations/languages/createall', translations.language_create_all, name='youradmin_translations_languages_create_all'),
    url(r'^translations/languages/helpersave', translations.translation_helper_edit, name='youradmin_translations_helper_save'),


    url(r'^cashflow/$', cashflow.cashflow, name='youradmin_cashflow_index'),
    url(r'^cashflow/upload$', cashflow.upload_csv, name='youradmin_cashflow_upload_csv'),

    # dashboard urls
    url(r'^dashboard/soldtickets$', dashboard.soldtickets, name='youradmin_dashboard_soldtickets'),

    # content
    url(r'^content/event_urls$', content.event_urls_index, name='youradmin_content_eventurls'),
    url(r'^content/event_urls/getlist$', content.event_urls_getlist, name='youradmin_content_eventurls_getlist'),
    url(r'^content/event_urls/create$', content.event_url_create, name='youradmin_content_eventurls_create'),
    url(r'^content/event_urls/(?P<dynamicurl_id>[-\w\.]+)/delete$', content.event_url_delete, name='youradmin_content_eventurls_delete'),
    url(r'^content/event_urls/(?P<dynamicurl_id>[-\w\.]+)/edit$', content.event_url_edit, name='youradmin_content_eventurls_edit'),
    url(r'^test$', orders.test, name='youradmin_test'),

    url(r'^financial/', include(([
            url(r'^$', financial.list_events, name='events'),
            url(r'^list$', financial.events_list, name='list'),
            url(r'^get_total$', financial.get_total_income, name='get_total'),
            url(r'^event/(?P<event_id>[-\w\.]+)/details', financial.get_event_details, name='get_event_detail'),
            url(r'^event/(?P<event_id>[-\w\.]+)/add_payment', financial.create_event_payment, name='add_event_payment'),
            url(r'^edit_payment/(?P<payment_id>[-\w\.]+)', financial.edit_event_payment, name='edit_event_payment'),
            url(r'^delete_payment/(?P<payment_id>[-\w\.]+)', financial.payment_delete, name='delete_event_payment'),
            url(r'^event/mark/(?P<event_id>[-\w\.]+)/', financial.mark_event, name='mark_event')
    ], 'youradmin_financial'))),

    url(r'^guestlist/', include(([
        url(r'^$', guestlist.index, name='index'),
        url(r'^list$', guestlist.getlist, name='list'),
        url(r'^send/(?P<id>[-\w\.]+)/$', guestlist.send, name='send'),

    ], 'youradmin_guestlist'))),

    url(r'^events/', include(([
        url(r'^$', events.index, name='index'),
        url(r'^list$', events.events_list, name='list'),
        url(r'update_totals', events.update_totals, name='update_totals')

    ], 'youradmin_events')))

]
